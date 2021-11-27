# CZ4010 Project Topic #7 : Demonstration of attacks on Substitution Permutation Network  Ciphers

# Motivation

This project aims to implement a reduced size Substitution Permutation Network (SPN), and to subsequently demonstrate an attack on the Cipher through Linear Cryptanalysis. The demonstrated attack will be a Known Plaintext Attack, where the attacker will have both the plaintext and their corresponding ciphertexts.

SPNs are a commonly used in block cipher algorithms such as AES. Therefore, it is important to study the strengths and weaknesses of this implementation.

Linear and Differential Cryptanalysis are commonly applied to block ciphers. In this demonstration, we will be focusing on Linear Cryptanalysis where we aim to find approximations to the action of a cipher.

# Research

For this project, a basic understanding of the SPN is required, as well as some research done on how Linear Cryptanalysis is implemented. Our implementation closely references the paper on [Linear (and Differential) Cryptanalysis by Howard M. Heys](https://ioactive.com/wp-content/uploads/2015/07/ldc_tutorial.pdf).

The paper demonstrates an attack on the [first substitution box chosen from the S-boxes of DES](https://en.wikipedia.org/wiki/DES_supplementary_material#Substitution_boxes_(S-boxes)). 

# Design

## File Structure

```
CZ4010-SPN-Cipher
└───images
|   |   linear equation 1(msb).png: tracing linear equation 1
|   |   linear equation 2(lsb).png: tracing linear equation 2
|   └───spn.png: implemented SPN design
| 
└───analysis.py: functions related to linear cryptanalysis
│   |   test_partial_key_eqn(): generates the number of times the equation holds true for each key
|   |   generate_test_keys(): generates all possible test keys combinations by concatenating 2 subkeys
|   |   test_encryption(): verifies if a known plaintext matches a decrypted ciphertext
|   |   generate_linear_approx_table(): generates the linear approximation table
|   └───calculate_bias(): calculates the bias for each subkey
| 
└───classes.py: classes used in implementing the SPN
|   |   SubBox: Substitution Box
|   |   PermBox: Permutation Box
|   └───SPN: Substitution Permutation Network
|   
└───data.py: contains known plaintext and ciphertext lists
|
└───LinearCryptanalysis.ipynb: notebook detailing the process of Known Plaintext Attack using Linear Cryptanalysis
|
└───README.md: project details
|
└───SPNetwork.ipynb: notebook detailing the usage of the project
|
└───utils.py: functions for general use
|   |   print_bits: for debugging purposes
|   |   print_bits_list: for debugging purposes
|   |   print_bit: for debugging purposes
|   |   convert_int_to_binary_array: converts an integer to its binary representation as an array
|   |   xor_binary_arrays: XORs 2 binary arrays
|   |   convert_binary_array_to_int: converts an array of binaries to its integer format
|   |   split_bits_to_4_bit_int: splits an integer into multiple 4-bit integers
|   |   visualise_linear_approx_table: creates a dataframe to present the linear approximation values
|   └───visualise_top_25_subkeys: visualises the linear attack bias table
```

## SPN Implementation

For our project, we implemented 4 layers to the SPN, with identical subtition boxes and permutation boxes being used across the layers. As the SPN takes in 16-bit plaintext input, 4 substitution boxes are used in each layer. Each layer uses identical round keys.

## Substitution Permutation Network

<p align="center">
    <img src="./images/spn.png" alt="Design of our SPN" width=80%/>
</p>

# Development

We created various python files to implement the necessary functions and classes to carry out our project.  

We then created 2 separate notebooks, SPNetwork.ipynb to showcase the implementation of the SPN, and LinearCryptanalysis.ipynb to demonstrate the Linear Cryptanalysis Attack on the implemented SPN.


## SPNetwork.ipynb

1. Encryption
    - We initialised an SPN object and the key
    - The plaintext is encrypted using the initialised SPN and key
2. Decryption
    - The ciphertext is decrypted using the same SPN and key

## LinearCryptanalysis.ipynb

1. Analysis of Cipher Components
    - We generated the linear approximation table for the Substitution Box in the SPN
2. Constructing Linear Approximations
    - Making use of the data from 1., we derived the linear equations for use in the Known Plaintext Attack for 2 subkeys corresponding to the first 8-bits and the last 8-bits of a 16-bit round key
    - The bias is then calculated for each subkey, and the highest subkeys are selected
3. Combining the subkeys
    - We test all combinations of the 2 groups of subkeys obtained from 2. by comparing encrypted known plaintexts (using the combined key) and their ciphertexts
    - Our implementation is successful as we manage to obtain the last round key
4. Limitations and Extensions
    - We detail the limitations of our project and describe how our project could be improved

# Usage of code

Users are strongly encouraged to first understand the usage of the SPN by running the [SPNetwork.ipynb](SPNetwork.ipynb) file. To better understand its implementation, users can refer to [classes.py](classes.py).

Afterwards, the user can then explore the implementation of the Known Plaintext Attack using Linear Cryptanalysis by following the steps detailed in the [LinearCryptanalysis.ipynb](LinearCryptanalysis.ipynb) file. To better understand the attack, users can refer to the [analysis.py](analysis.py) file.

For other functions used in this project, users can refer to the [utils.py](utils.py) file.

A visualisation of how the linear equations were derived can be found in the [images](./images/) folder.