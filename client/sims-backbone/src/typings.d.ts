/* SystemJS module definition */
declare var module: NodeModule;
interface NodeModule {
id: string;
}
declare var sprocess: Process;

interface Process {
env: Env
}

interface Env {
            GOOGLE_API_KEY: string
            CLIENT_ID: string
            CLIENT_SECRET: string
            SIMS_REDIRECT_URI: string
            BACKBONE_API_LOCATION: string
}

interface GlobalEnvironment{
process: Process;
}
