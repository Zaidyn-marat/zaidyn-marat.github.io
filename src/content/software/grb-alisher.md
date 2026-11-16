---
name: "grb_reconstruction"
repo: "https://github.com/Wanamee/grb_reconstruction"
language: "Python"
summary: "Deep learning architectures (BiLSTM, TCN, BiGRU) for reconstructing observational gaps and plateau phases in Swift gamma-ray burst light curves."
paper: "https://doi.org/10.31489/2025N4/132-142"
---

A sequence modeling pipeline for imputing missing segments and reconstructing sparse gamma-ray burst (GRB) light curves from Swift XRT and UVOT observations.

The repository includes data cleaning utilities (`swiftxrt_clean.py`), benchmark implementations of Bidirectional LSTM (`bilstm.py`), Bidirectional GRU (`gru.py`), and Temporal Convolutional Networks (`TCN.py`), as well as light-curve reconstruction scripts (e.g., `GRB050713Afig.py`) to support plateau-phase modeling and cosmological parameter estimation.