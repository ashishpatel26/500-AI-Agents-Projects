# Governance Consensus Agent (Parliament of Minds)

A multi-model consensus agent that runs a question across N models at 3 different temperatures (0.1, 0.5, 0.8) in parallel. It uses cross-agreement weighting (Jaccard similarity) and an adversarial cross-check to achieve high confidence in outputs. 

## Architecture

```text
       [ Input Question ]
              |
      +-------+-------+
      |               |
[ Model A ]     [ Model B ] ... (N models)
  |  |  |         |  |  |   --- (Temperatures: 0.1, 0.5, 0.8)
  v  v  v         v  v  v
 [ Response Pool (3 * N) ]
              |
   [ Constitution Veto Check ]
              |
 [ Cross-Agreement Weighting ] (Jaccard Similarity)
              |
   [ Adversarial Cross-Check ] (Critique Phase)
              |
       [ Final Output ]
```

## Governance Modes

| Mode | Description |
|---|---|
| **Democracy** | All models vote across temperatures + adversarial cross-check. The most agreeable response wins. |
| **Oligarchy** | Top 2 models/responses must agree with a similarity > 0.5 to pass. |
| **Dictatorship** | The fastest model response is accepted immediately. |
| **Theocracy** | Strict constitutional veto. Responses are heavily penalized or rejected if they violate the constitution regex. |
| **Monarchy** | A sovereign (main model) generates the primary answer, and a court of 3 advisors critique it. |

## Constitution Explanation

The system uses a strict Regex-based constitution that instantly vetoes responses containing forbidden patterns:
- Destructive commands: `rm -rf`, `format C:`, `del /f`
- Secrets/PII: `password=".*"`, `api_key=".*"`
- Dangerous financial advice: `double down`, `full margin`, `all in`

## Quick Start

1. Set up environment variables in `.env` (or copy from `.env.example`).
2. Run the agent:

```bash
python agent.py --mode democracy "What is the capital of France?"
```

## Sample Output

### Democracy Mode
```
[Democracy] Gathering votes...
[Democracy] 6/6 responses passed constitution.
[Democracy] Running adversarial cross-check...
Final Output (Democracy | Confidence: 92/100):
The capital of France is Paris.
```

### Theocracy Mode
```
[Theocracy] Seeking divine answer...
[Constitution] VETO: Response contained forbidden string.
Final Output (Theocracy | Confidence: 0/100):
BLOCKED BY CONSTITUTION.
```

## Standard Multi-Agent vs Governance Consensus

| Feature | Standard Multi-Agent | Governance Consensus Agent |
|---|---|---|
| **Voting** | Simple Majority | Cross-Agreement (Jaccard) |
| **Safety** | Prompt-based | Regex Constitution Veto |
| **Confidence** | N/A | Calculated (0-100) |
| **Execution** | Sequential | Parallel (ThreadPoolExecutor) |

## Safety Notes

This agent is designed with a strict constitution to prevent destructive actions or the leaking of sensitive information. However, regex matching is not foolproof. Always run within a sandboxed environment if executing code.

## Performance Specs

- **Dependencies**: 0 (Pure Python stdlib)
- **Concurrency**: `concurrent.futures.ThreadPoolExecutor`
- **Supported Python**: 3.8+

## License

MIT License

## Author
Irfan Fahmi (github.com/l3al3y)
