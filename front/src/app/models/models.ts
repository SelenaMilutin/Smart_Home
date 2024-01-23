export interface PiComponent {
    code: string
    simulated: boolean,
    runsOn: string,
    name: string,
    measurement: string[],
    topic: string[],
    value: number | string,
    timestamp: string | null,
}

export interface PI {
    name: string
}