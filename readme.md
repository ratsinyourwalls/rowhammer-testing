# Rowhammer-Testing
Testing simulator for various protector strategies

## Modules
- Memory: simulates a memory with varing sizes and reads/writes
- Controller: simulates a memory controller, handling refreshes
- Protector: simulates a rowhammer protection, getting notified on
  writes/refreshes
- test: main code, inputs the write sequence and generates a report
