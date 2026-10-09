"""Detect people in the three showcase clips and draw temporary tracking IDs.

Business metrics are not computed here. The marketing renderer overlays fictional
cards separately. IDs reset at each scene; no facial or cross-scene identity.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cafe_analytics.detector import Detector
from cafe_analytics.tracker import Tracker
from render_marketing_demo import SCENES


def main():
    out = Path('runs/showcase-tracking')
    out.mkdir(parents=True, exist_ok=True)
    model = Path('models/yolox_s.onnx')
    detector = Detector(model, threshold=0.15, threads=4)
    scenes = []
    for index, (name, source, _) in enumerate(SCENES):
        normalized = out / f'{index}-source.mp4'
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',source,'-t','9','-vf','scale=1280:720,setsar=1,fps=30','-an','-c:v','libx264','-crf','18',str(normalized)],check=True)
        cap = cv2.VideoCapture(str(normalized))
        target = out / f'{index}.mp4'
        writer = cv2.VideoWriter(str(target),cv2.VideoWriter_fourcc(*'mp4v'),30,(1280,720))
        if not cap.isOpened() or not writer.isOpened():
            raise RuntimeError('Cannot open input/output video')
        tracker = Tracker(high_score=0.50)
        rows=[]
        frame_index=0
        tracks=[]
        prefixes=['C','R','T']
        try:
            while True:
                ok, frame = cap.read()
                if not ok: break
                if frame_index % 3 == 0:
                    tracks=tracker.update(detector(frame),frame_index/30)
                observations=[]
                for track in tracks:
                    box=np.rint(track.box).astype(int)
                    x1,y1,x2,y2=box
                    x1,x2=np.clip([x1,x2],0,1279);y1,y2=np.clip([y1,y2],0,719)
                    if x2<=x1 or y2<=y1: continue
                    tint=(175,245,157) if track.id%2 else (240,220,75)
                    cv2.rectangle(frame,(x1,y1),(x2,y2),tint,1,cv2.LINE_AA)
                    size=min(20,max(5,(x2-x1)//4),max(5,(y2-y1)//4))
                    for x,dx in [(x1,1),(x2,-1)]:
                        for y,dy in [(y1,1),(y2,-1)]:
                            cv2.line(frame,(x,y),(x+dx*size,y),tint,3,cv2.LINE_AA)
                            cv2.line(frame,(x,y),(x,y+dy*size),tint,3,cv2.LINE_AA)
                    label=f'ID {prefixes[index]}-{track.id:03d}'
                    (tw,th),baseline=cv2.getTextSize(label,cv2.FONT_HERSHEY_SIMPLEX,.55,1)
                    lx=min(x1,1279-tw-16);ly=max(28,y1)
                    cv2.rectangle(frame,(lx,ly-27),(lx+tw+14,ly-1),(25,46,33),-1)
                    cv2.putText(frame,label,(lx+7,ly-8),cv2.FONT_HERSHEY_SIMPLEX,.55,tint,1,cv2.LINE_AA)
                    point=((x1+x2)//2,y2)
                    if track.trail and np.linalg.norm(np.array(point)-track.trail[-1])>150:
                        track.trail.clear()
                    track.trail.append(point)
                    trail=list(track.trail)[-18:]
                    if len(trail)>1:cv2.polylines(frame,[np.array(trail,np.int32)],False,tint,1,cv2.LINE_AA)
                    cv2.circle(frame,point,3,tint,-1,cv2.LINE_AA)
                    observations.append({'id':label,'box':[int(x1),int(y1),int(x2),int(y2)],'detector_score':round(track.score,4)})
                rows.append({'frame':frame_index,'time_s':round(frame_index/30,4),'people':observations})
                writer.write(frame);frame_index+=1
                if frame_index%90==0:print(f'{name}: {frame_index}/270 frames',flush=True)
        finally:
            writer.release();cap.release()
        if frame_index!=270:raise RuntimeError(f'Expected 270 frames, got {frame_index}')
        scenes.append({'scene':index,'business':name,'source_sha256':hashlib.sha256(Path(source).read_bytes()).hexdigest(),'frames':frame_index,'frames_with_boxes':sum(bool(row['people']) for row in rows),'max_simultaneous_boxes':max(len(row['people']) for row in rows),'observations':rows})
    (out/'tracking.json').write_text(json.dumps({'type':'actual_person_detector_tracking','inference_fps':10,'video_fps':30,'intermediate_frames':'hold last detected boxes for at most 2 frames','model_sha256':hashlib.sha256(model.read_bytes()).hexdigest(),'ids_are_temporary':True,'business_cards_are_not_inferred':True,'scenes':scenes},ensure_ascii=False,separators=(',',':')))
    print('Tracking complete',flush=True)


if __name__=='__main__':main()
