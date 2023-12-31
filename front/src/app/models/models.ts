export interface PiComponent {
    code: string
    simulated: boolean,
    runsOn: string,
    name: string,
    measurement: string[],
    topic: string[]
}

export interface PI {
    name: string
}