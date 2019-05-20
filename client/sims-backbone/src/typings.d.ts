/* SystemJS module definition */
declare var module: NodeModule;
interface NodeModule {
id: string;
}
declare var process: Process;

interface Process {
env: Env
}

interface Env {
            GOOGLE_API_KEY: string
            CLIENT_ID: string
            CLIENT_SECRET: string
}

interface GlobalEnvironment{
process: Process;
}
