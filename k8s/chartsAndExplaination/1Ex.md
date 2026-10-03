# Kubernetes Orchestration Flow

## Without Orchestration

```mermaid
graph TB
    S[Server]
    S --> CA[Container A ✓]
    S --> CB[Container B ❌]
    S --> CC[Container C ✓]
    
    M[Monitoring detects failure]
    M --> E1[Engineer receives alert]
    E1 --> E2[Engineer connects to server]
    E2 --> R[Container restarted]
    
    style S fill:#2E4057,stroke:#1B2631,color:#fff
    style CA fill:#28B463,stroke:#1E8449,color:#fff
    style CB fill:#E74C3C,stroke:#C0392B,color:#fff
    style CC fill:#28B463,stroke:#1E8449,color:#fff
    style M fill:#F39C12,stroke:#D68910,color:#000
    style E1 fill:#E67E22,stroke:#CA6F1E,color:#fff
    style E2 fill:#E67E22,stroke:#CA6F1E,color:#fff
    style R fill:#3498DB,stroke:#2874A6,color:#fff
```

## With Kubernetes

```mermaid
graph TB
    DS[Desired State = 3 replicas]
    CS1[Current State = 2 replicas]
    
    DS -.->|continuously compares| KC[Kubernetes Controller]
    CS1 -.->|continuously compares| KC
    
    KC --> CR[Creates replacement]
    CR --> CS2[Current State = 3 replicas]
    
    style DS fill:#3498DB,stroke:#2874A6,color:#fff
    style CS1 fill:#E74C3C,stroke:#C0392B,color:#fff
    style KC fill:#9B59B6,stroke:#7D3C98,color:#fff
    style CR fill:#F39C12,stroke:#D68910,color:#000
    style CS2 fill:#28B463,stroke:#1E8449,color:#fff
```

## Key Concept: Reconciliation Loop

```mermaid
graph TB
    KC[Kubernetes Controller]
    KC -.->|monitors| Desired[Desired State]
    KC -.->|monitors| Actual[Actual State]
    KC -->|reconciles| Action[Automatic Action]
    
    style KC fill:#9B59B6,stroke:#7D3C98,color:#fff
    style Desired fill:#3498DB,stroke:#2874A6,color:#fff
    style Actual fill:#F39C12,stroke:#D68910,color:#000
    style Action fill:#28B463,stroke:#1E8449,color:#fff
```

## Important Concept

**Kubernetes continuously compares desired state with actual state** and automatically takes action to reconcile any differences.

### Without Orchestration:
- **Manual intervention required**
- Downtime until engineer responds
- Human error possible
- Slower recovery time

### With Kubernetes:
- **Automatic self-healing**
- Immediate detection and response
- Consistent and reliable
- Faster recovery time
