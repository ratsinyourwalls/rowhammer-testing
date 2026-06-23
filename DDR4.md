# DRAM version 4

### Organization

A memory controller can interface with multiple DRAM ranks by time-multiplexing the channel's I/O bus between the ranks. A DRAM rank comprises multiple DRAM *chips* that operate in lockstep. The combined data pins from all chips form the DRAM data bus.

Within a chip, cells are organized hierarchically to provide high density and performance. A DRAM chip is composed of multiple (for example 8 or 16) DRAM *banks*.

A bank comprises many(e.g. 128) subarrays. Each subarray contains a two-dimentional array of DRAM cells arranged in *rows* and *columns*.

For our simulation we are only considering a single DRAM chip with 4 banks and ignoring subarrays.


**DRAM Refresh** Cells throughout a DRAM chip have different retention times, ranging from milliseconds to hours.

DRAM refresh is typically every 32 or 64 ms according to DRAM specifications.
We don't actually use real time, but we count the number of reads to define the refresh cycle.
