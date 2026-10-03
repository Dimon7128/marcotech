# Kubernetes Orchestration Flow

## Without Orchestration vs With Kubernetes

```mermaid
graph TB
    subgraph "Without Orchestration"
        S[Server]
        S --> CA[Container A ✓]
        S --> CB[Container B ❌]
        S --> CC[Container C ✓]
        
        M[Monitoring detects failure]
        M --> E1[Engineer receives alert]
        E1 --> E2[Engineer connects to server]
        E2 --> R[Container restarted]
    end
    
    subgraph "With Kubernetes"
        DS[Desired State = 3 replicas]
        CS1[Current State = 2 replicas]
        
        DS -.->|continuously compares| KC[Kubernetes Controller]
        CS1 -.->|continuously compares| KC
        
        KC --> CR[Creates replacement]
        CR --> CS2[Current State = 3 replicas]
    end
    
    subgraph "Key Concept"
        KC2[Kubernetes Controller]
        KC2 -.->|monitors| Desired[Desired State]
        KC2 -.->|monitors| Actual[Actual State]
        KC2 -->|reconciles| Action[Automatic Action]
    end
    
    style CB fill:#ff9999
    style DS fill:#99ccff
    style CS2 fill:#99ff99
    style KC fill:#ffcc99
    style KC2 fill:#ffcc99
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
