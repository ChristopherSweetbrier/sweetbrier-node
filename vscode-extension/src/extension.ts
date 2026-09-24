import * as path from "path";
import { ExtensionContext, workspace } from "vscode";
import { LanguageClient, LanguageClientOptions, ServerOptions } from "vscode-languageclient/node";

let client: LanguageClient;

export function activate(context: ExtensionContext) {
    console.log("Sweetbrier Epistemic Firewall LSP is now active!");

    // The path to the Python server script we wrote earlier
    // Assuming the python script is in the root of the workspace
    const serverPath = context.asAbsolutePath(path.join("..", "sweetbrier_lsp.py"));

    // We start the Python process via stdio
    const serverOptions: ServerOptions = {
        command: "python",
        args: [serverPath],
    };

    // Options to control the language client
    const clientOptions: LanguageClientOptions = {
        documentSelector: [
            { scheme: "file", language: "mermaid" },
            { scheme: "file", language: "markdown" }
        ],
        synchronize: {
            fileEvents: workspace.createFileSystemWatcher("**/*.{md,mmd}")
        }
    };

    // Create the language client and start the client.
    client = new LanguageClient(
        "sweetbrierLsp",
        "Sweetbrier Language Server",
        serverOptions,
        clientOptions
    );

    client.start();
}

export function deactivate(): Thenable<void> | undefined {
    if (!client) {
        return undefined;
    }
    return client.stop();
}
