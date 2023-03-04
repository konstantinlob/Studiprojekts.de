import { useState } from "react";
import YearSelectionInput from "./YearSelection";
import YearSwitcherInput from "./YearSwitcher";

export enum YearInputModes {
    switcher,
    selection,
}

const modeMap = {
    [YearInputModes.switcher]: YearSwitcherInput,
    [YearInputModes.selection]: YearSelectionInput,
};

export default function YearInputHandler() {
    const [mode, setMode] = useState<YearInputModes>(YearInputModes.switcher);

    const InputComponent = modeMap[mode];

    return <div className="flex flex-col gap-1 p-1">
        <Switch currentMode={mode} setMode={setMode} />
        <InputComponent />
    </div>;
}


interface SwitchProps {
    currentMode: YearInputModes
    setMode: (m: YearInputModes) => void
}

function Switch({ currentMode, setMode }: SwitchProps) {
    const options: Array<[number, string]> = [
        [YearInputModes.selection, "Advanced"],
        [YearInputModes.switcher, "Simple"],
    ];

    return <div className="text-xs py-px flex justify-evenly gap-2 bg-fgc bg-opacity-20 rounded-lg overflow-hidden">
        {options.map(([mode, text]) => {
            const isCurrent = mode === currentMode;
            return <button key={text} className="grow relative grid place-content-center" onClick={() => setMode(mode)} style={{cursor: isCurrent ? "default" : "pointer"}}>
                <div className="bg-fgc bg-opacity-20 absolute inset-0" style={{visibility: isCurrent ? "initial" : "hidden"}} />
                <div className="z-10">
                    {text}
                </div>
            </button>;
        })}
    </div>;
}
