# How to Set Up a Sweetbrier Node (Zero-Jargon Quickstart)

You do not need a PhD in machine learning to run a safe, deterministic AI. If you can draw a flowchart and copy-paste a few lines of text, you can deploy a Sweetbrier Node. 

Sweetbrier is an **Epistemic Firewall**. It physically cages an AI inside a visual flowchart (a DAG) so it cannot hallucinate or drift off-topic. Here is how to set one up on your own computer in 5 minutes.

---

### Step 1: Install the Engine (Ollama)
We run the AI locally on your computer so your data stays private and you don't pay API fees.
1. Go to [Ollama.com](https://ollama.com/) and download the app for Windows or Mac.
2. Install it like any normal program.

### Step 2: Download the Brain (Hermes-3)
We need an open-source AI model to put inside the firewall. We use `hermes3:8b` because it is smart, fast, and uncensored (meaning our structural firewall does the safety work, not hidden corporate filters).
1. Open your Terminal (Mac) or Command Prompt (Windows).
2. Type this exact command and hit Enter:
   ```bash
   ollama run hermes3:8b
   ```
3. It will download the model. Once it says "Success", you can close the terminal.

### Step 3: Get the Sweetbrier Firewall
1. Download this GitHub repository (Click the green "Code" button -> Download ZIP) and extract it to a folder.
2. Open your Terminal/Command prompt, navigate to that folder, and install the one requirement we need for the graph math (`networkx`):
   ```bash
   pip install networkx
   ```

### Step 4: Draw Your Boundaries (Visual Programming)
Sweetbrier uses Mermaid.js, a simple way to draw flowcharts using text. 
1. Open a text file and draw the boundaries you want your AI to have. Here is a simple example:
   ```mermaid
   graph TD
       A[User Asks Question] --> B{Intent Router}
       B --> C[Fetch Allowed Documents]
       B -.-> D[Hallucinate/Guess]
       D -.-> E((Sweetbrier Firewall Blocks This))
       C --> F[Output Safe Answer]
   ```
2. Save this text as `my_chart.txt`. 

### Step 5: Compile and Run!
Now, we turn your drawing into executable code.
1. In your terminal, run the compiler:
   ```bash
   python harness/mermaid_compiler.py
   ```
2. The compiler will read your flowchart, mathematically verify that it is safe (no infinite loops), and build the **Sweetbrier Topology JSON**.
3. You now have a fully functional Sweetbrier Node! You can pass prompts into the Sweetbrier engine, and it will physically refuse to process any path that strays outside the flowchart you just drew. 

Welcome to the future of deterministic, insurable AI. 
