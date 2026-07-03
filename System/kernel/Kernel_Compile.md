# Kernel Compilation Guide

## Step 1: Download Kernel Version
Download your target kernel version from [Kernel.org](https://www.kernel.org).

## Step 2: Extract Kernel File
```bash
tar -xvf linux-6.0.tar.xz
```

## Step 3: Copy Current Kernel Configure
Copy current kernel configuration to the new kernel directory.
```bash
cp -v /boot/config-$(uname -r) .config
```

## Step 4: Install Dependencies
Install necessary dependencies.
```bash
sudo apt-get install git fakeroot build-essential ncurses-dev xz-utils libssl-dev bc flex libelf-dev bison dwarves
```

## Step 5: Disable Conflicting Security Certificates (For Ubuntu)
If you are using Ubuntu, disable conflicting security certificates.
```bash
scripts/config --disable SYSTEM_TRUSTED_KEYS && scripts/config --disable SYSTEM_REVOCATION_KEYS
```

## Step 6: Make Menu Configure
Configure kernel options using menuconfig.
```bash
make menuconfig
```

## Step 7: Compile Main Files
Compile main kernel files.
```bash
make -j<CPU Core Yo Give Compiler>
```

## Step 8: Compile Modules Files
Compile kernel modules.
```bash
make modules -j<CPU Core Yo Give Compiler>
```

## Step 9: Compile Modules Install Files
Compile and install kernel modules.
```bash
make modules_install -j<CPU Core Yo Give Compiler>
```

## Step 10: Install Compiled File
Install compiled kernel.
```bash
make install -j<CPU Core Yo Give Compiler>
```

