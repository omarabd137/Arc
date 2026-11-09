import { Composition } from "remotion";
import { MyComposition } from "./Composition";
import { PersonTest } from "./overbooking/PersonTest";
import { Overbooking, ContactSheet } from "./overbooking/Overbooking";
import { DURATION_FRAMES, FPS, W, H } from "./overbooking/timing";

const SHEET1 = [0, 26, 70, 92, 150, 186, 268, 345, 440, 478, 540, 650, 812, 850, 905, 985];
const SHEET2 = [1030, 1060, 1105, 1150, 1185, 1205, 1240, 1275, 1300, 1326, 120, 230, 300, 400, 600, 700];

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <MyComposition />
      <Composition id="PersonTest" component={PersonTest} durationInFrames={30} fps={30} width={1080} height={1920} />
      <Composition id="Overbooking" component={Overbooking} durationInFrames={DURATION_FRAMES} fps={FPS} width={W} height={H} />
      <Composition id="Sheet1" component={ContactSheet} defaultProps={{ frames: SHEET1 }} durationInFrames={DURATION_FRAMES} fps={FPS} width={W} height={H} />
      <Composition id="Sheet2" component={ContactSheet} defaultProps={{ frames: SHEET2 }} durationInFrames={DURATION_FRAMES} fps={FPS} width={W} height={H} />
    </>
  );
};
