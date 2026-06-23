# Rowhammer-Testing
Testing simulator for various protector strategies

## Modules
- Memory: simulates a memory with varying sizes and reads/writes
- Controller: simulates a memory controller, handling refreshes
- Protector: simulates a Rowhammer protection, getting notified on
  writes/refreshes
- test: main code, inputs the write sequence and generates a report

## Rowhammer mitigation strategies
- `para_protector` implements PARA.
- `graphene_protector` implements Graphene.

