import { AbsoluteFill } from "remotion";
import { Person, GUY, AGENT, CROWD, SEATED_WOMAN } from "./kit/Person";

export const PersonTest: React.FC = () => (
  <AbsoluteFill style={{ background: "linear-gradient(#BFE0F2, #FFD9A6)" }}>
    <Person look={GUY} x={260} y={820} h={700} itemR="pass" pose={{ armR: 40, elbowR: -70 }} expr={{ brows: 1, mouth: "smile" }} />
    <Person look={AGENT} x={760} y={820} h={700} itemR="mic" pose={{ armR: 30, elbowR: -100 }} expr={{ mouth: "open" }} seed={3} />
    <Person look={GUY} x={260} y={1620} h={700} itemR="cash" pose={{ armR: 160, elbowR: 10, armL: 30 }} expr={{ mouth: "grin", eyes: "happy" }} seed={5} />
    <Person look={CROWD[0]} x={620} y={1620} h={600} pose={{ crossed: true }} expr={{ mouth: "flat", brows: -0.4 }} seed={7} />
    <Person look={SEATED_WOMAN} x={900} y={1620} h={600} pose={{ sit: true }} expr={{ mouth: "smile", eyes: "happy" }} seed={9} />
  </AbsoluteFill>
);
