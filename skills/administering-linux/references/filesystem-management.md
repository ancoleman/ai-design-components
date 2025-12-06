# Filesystem Management Guide

Complete reference for managing Linux filesystems, LVM, RAID, permissions, and storage.

## Table of Contents

1. [Filesystem Types](#filesystem-types)
2. [Logical Volume Manager (LVM)](#logical-volume-manager-lvm)
3. [RAID Configuration](#raid-configuration)
4. [Mounting and fstab](#mounting-and-fstab)
5. [Permissions and ACLs](#permissions-and-acls)
6. [Disk Usage Management](#disk-usage-management)

## Filesystem Types

### Comparison

| Filesystem | Best For | Max File Size | Snapshots | Notes |
|------------|----------|---------------|-----------|-------|
| **ext4** | General purpose | 16 TB | No | Default on most distros, mature |
| **XFS** | Large files, databases | 8 EB | No | RHEL default, excellent performance |
| **Btrfs** | Snapshots, CoW | 16 EB | Yes | Modern features, copy-on-write |
| **ZFS** | Enterprise, data integrity | 16 EB | Yes | Not in mainline kernel, NAS/storage |

### Creating Filesystems

**ext4:**
```bash
sudo mkfs.ext4 /dev/sdb1
sudo mkfs.ext4 -L mylabel /dev/sdb1     # With label
```

**XFS:**
```bash
sudo mkfs.xfs /dev/sdb1
sudo mkfs.xfs -L mylabel /dev/sdb1
```

**Btrfs:**
```bash
sudo mkfs.btrfs /dev/sdb1
sudo mkfs.btrfs -L mylabel /dev/sdb1
```

## Logical Volume Manager (LVM)

### LVM Concepts

**Three layers:**
1. **Physical Volumes (PV)** - Raw disks/partitions
2. **Volume Groups (VG)** - Pool of PVs
3. **Logical Volumes (LV)** - Virtual partitions from VG

### Creating LVM Setup

**Step 1: Create Physical Volume**
```bash
sudo pvcreate /dev/sdb
sudo pvcreate /dev/sdc

# View PVs
sudo pvdisplay
sudo pvs
```

**Step 2: Create Volume Group**
```bash
sudo vgcreate vg_data /dev/sdb /dev/sdc

# View VGs
sudo vgdisplay
sudo vgs
```

**Step 3: Create Logical Volume**
```bash
# Fixed size
sudo lvcreate -L 10G -n lv_data vg_data

# Percentage of VG
sudo lvcreate -l 100%FREE -n lv_data vg_data

# View LVs
sudo lvdisplay
sudo lvs
```

**Step 4: Create Filesystem**
```bash
sudo mkfs.ext4 /dev/vg_data/lv_data
```

**Step 5: Mount**
```bash
sudo mkdir /mnt/data
sudo mount /dev/vg_data/lv_data /mnt/data
```

### Extending LVM Volumes

**Extend LV:**
```bash
# Add 5GB
sudo lvextend -L +5G /dev/vg_data/lv_data

# Use all free space
sudo lvextend -l +100%FREE /dev/vg_data/lv_data
```

**Resize Filesystem:**
```bash
# ext4
sudo resize2fs /dev/vg_data/lv_data

# XFS
sudo xfs_growfs /mnt/data

# Btrfs
sudo btrfs filesystem resize max /mnt/data
```

**One-step extend and resize:**
```bash
sudo lvextend -L +5G --resizefs /dev/vg_data/lv_data
```

### Reducing LVM Volumes

**WARNING:** Can cause data loss if not careful!

**For ext4 only (XFS cannot shrink):**
```bash
# Unmount first
sudo umount /mnt/data

# Check filesystem
sudo e2fsck -f /dev/vg_data/lv_data

# Resize filesystem first
sudo resize2fs /dev/vg_data/lv_data 8G

# Then reduce LV
sudo lvreduce -L 8G /dev/vg_data/lv_data

# Remount
sudo mount /dev/vg_data/lv_data /mnt/data
```

### LVM Snapshots

```bash
# Create snapshot (10% of original size for changes)
sudo lvcreate -L 1G -s -n lv_data_snap /dev/vg_data/lv_data

# Mount snapshot
sudo mkdir /mnt/snapshot
sudo mount /dev/vg_data/lv_data_snap /mnt/snapshot

# Restore from snapshot
sudo lvconvert --merge /dev/vg_data/lv_data_snap

# Remove snapshot
sudo lvremove /dev/vg_data/lv_data_snap
```

## RAID Configuration

### RAID Levels

| Level | Description | Min Disks | Usable Space | Fault Tolerance |
|-------|-------------|-----------|--------------|-----------------|
| RAID 0 | Striping | 2 | 100% | None (any disk failure = data loss) |
| RAID 1 | Mirroring | 2 | 50% | N-1 disks |
| RAID 5 | Striping + parity | 3 | (N-1)/N | 1 disk |
| RAID 6 | Striping + double parity | 4 | (N-2)/N | 2 disks |
| RAID 10 | Mirror + stripe | 4 | 50% | 1 disk per mirror |

### Creating Software RAID with mdadm

**Install mdadm:**
```bash
sudo apt install mdadm              # Ubuntu/Debian
sudo dnf install mdadm              # RHEL/Fedora
```

**Create RAID 1 (mirroring):**
```bash
sudo mdadm --create /dev/md0 \
    --level=1 \
    --raid-devices=2 \
    /dev/sdb /dev/sdc

# Monitor creation
watch cat /proc/mdstat
```

**Create RAID 5:**
```bash
sudo mdadm --create /dev/md0 \
    --level=5 \
    --raid-devices=3 \
    /dev/sdb /dev/sdc /dev/sdd
```

**Create filesystem and mount:**
```bash
sudo mkfs.ext4 /dev/md0
sudo mkdir /mnt/raid
sudo mount /dev/md0 /mnt/raid
```

**Save RAID configuration:**
```bash
sudo mdadm --detail --scan | sudo tee -a /etc/mdadm/mdadm.conf
sudo update-initramfs -u
```

**Check RAID status:**
```bash
cat /proc/mdstat
sudo mdadm --detail /dev/md0
```

**Add spare disk:**
```bash
sudo mdadm --add /dev/md0 /dev/sde
```

**Remove failed disk:**
```bash
sudo mdadm --fail /dev/md0 /dev/sdb
sudo mdadm --remove /dev/md0 /dev/sdb
# Replace disk
sudo mdadm --add /dev/md0 /dev/sdf
```

## Mounting and fstab

### Manual Mounting

```bash
# Mount filesystem
sudo mount /dev/sdb1 /mnt/data

# Mount with options
sudo mount -o rw,noexec,nosuid /dev/sdb1 /mnt/data

# Mount by label
sudo mount LABEL=mylabel /mnt/data

# Mount by UUID
sudo mount UUID=xxxx-xxxx /mnt/data

# Remount with different options
sudo mount -o remount,ro /mnt/data

# Unmount
sudo umount /mnt/data
```

### /etc/fstab Configuration

**Format:**
```
<device> <mount_point> <type> <options> <dump> <pass>
```

**Examples:**
```bash
# /etc/fstab

# By device
/dev/sdb1  /mnt/data  ext4  defaults  0  2

# By UUID (recommended)
UUID=xxx-xxx  /mnt/data  ext4  defaults  0  2

# By label
LABEL=mylabel  /mnt/data  ext4  defaults  0  2

# With specific options
UUID=xxx  /mnt/data  ext4  rw,noexec,nosuid  0  2

# NFS mount
server:/export  /mnt/nfs  nfs  defaults  0  0

# Temporary filesystem
tmpfs  /tmp  tmpfs  defaults,noatime,mode=1777  0  0
```

**Common mount options:**
- `defaults` - rw, suid, dev, exec, auto, nouser, async
- `ro` - Read-only
- `rw` - Read-write
- `noexec` - Don't allow program execution
- `nosuid` - Ignore SUID bits
- `nodev` - Don't interpret block special devices
- `noatime` - Don't update access time (performance)
- `nodiratime` - Don't update directory access time
- `nofail` - Don't fail boot if device missing

**Apply fstab changes:**
```bash
sudo mount -a                      # Mount all in fstab
sudo findmnt --verify              # Verify fstab syntax
```

## Permissions and ACLs

### Standard Permissions

**Permission types:**
- **r** (4) - Read
- **w** (2) - Write
- **x** (1) - Execute

**Three groups:**
- Owner
- Group
- Others

**Examples:**
```bash
# Symbolic
chmod u+x file                     # Add execute for user
chmod g+w file                     # Add write for group
chmod o-r file                     # Remove read for others
chmod a+x file                     # Add execute for all

# Numeric
chmod 644 file                     # rw-r--r--
chmod 755 file                     # rwxr-xr-x
chmod 600 file                     # rw-------
chmod 777 file                     # rwxrwxrwx (avoid!)

# Recursive
chmod -R 755 directory
```

**Change ownership:**
```bash
chown user file                    # Change owner
chown user:group file              # Change owner and group
chown -R user:group directory      # Recursive
chgrp group file                   # Change group only
```

**Special permissions:**
```bash
# SUID (Set User ID) - 4000
chmod u+s executable               # Run as file owner
chmod 4755 executable

# SGID (Set Group ID) - 2000
chmod g+s executable               # Run as file group
chmod g+s directory                # New files inherit directory group
chmod 2755 directory

# Sticky bit - 1000
chmod +t directory                 # Only owner can delete files
chmod 1777 /tmp                    # Typical for /tmp
```

### Access Control Lists (ACLs)

Extended permissions beyond standard owner/group/other.

**View ACLs:**
```bash
getfacl file
```

**Set ACLs:**
```bash
# Give user specific permissions
setfacl -m u:username:rw file

# Give group specific permissions
setfacl -m g:groupname:rx file

# Remove ACL
setfacl -x u:username file

# Remove all ACLs
setfacl -b file

# Default ACLs for directory (inherited by new files)
setfacl -d -m u:username:rw directory

# Recursive
setfacl -R -m u:username:rw directory
```

**Copy ACLs:**
```bash
getfacl file1 | setfacl --set-file=- file2
```

## Disk Usage Management

### Checking Disk Usage

**Filesystem usage:**
```bash
df -h                              # Human-readable
df -i                              # Inode usage
df -T                              # Show filesystem type
df -h /path                        # Specific mount point
```

**Directory usage:**
```bash
du -sh /path                       # Summary
du -h --max-depth=1 /path          # One level deep
du -sh /* | sort -h                # Sort by size
ncdu /path                         # Interactive (requires install)
```

**Find large files:**
```bash
find /path -type f -size +100M     # Files > 100MB
find /path -type f -size +100M -exec ls -lh {} \;

# Top 10 largest files
find /path -type f -exec du -h {} + | sort -rh | head -10
```

**Find large directories:**
```bash
du -h /path | sort -rh | head -20
```

### Cleaning Up Disk Space

**Log files:**
```bash
# Find large logs
find /var/log -type f -size +10M

# Truncate logs (don't delete - may break apps)
sudo truncate -s 0 /var/log/large.log

# Rotate logs
sudo logrotate -f /etc/logrotate.conf

# Clean systemd journal
sudo journalctl --vacuum-size=500M
sudo journalctl --vacuum-time=7d
```

**Package caches:**
```bash
# Ubuntu/Debian
sudo apt clean
sudo apt autoremove

# RHEL/Fedora
sudo dnf clean all
```

**Temp files:**
```bash
sudo find /tmp -type f -atime +7 -delete
sudo find /var/tmp -type f -atime +30 -delete
```

**Deleted files still open:**
```bash
# Find processes holding deleted files
sudo lsof | grep deleted

# Restart service to release
systemctl restart service_name
```

## Best Practices

1. **Always use UUIDs in fstab** (device names can change)
2. **Test fstab with `mount -a`** before rebooting
3. **Backup data before LVM operations**
4. **Use LVM for flexibility** (easy to resize)
5. **Monitor RAID arrays** regularly
6. **Set appropriate permissions** (principle of least privilege)
7. **Use noatime/nodiratime** for performance
8. **Regular filesystem checks** (fsck during maintenance windows)

## References

- mount(8): `man mount`
- fstab(5): `man fstab`
- lvm(8): `man lvm`
- mdadm(8): `man mdadm`
- chmod(1): `man chmod`
- setfacl(1): `man setfacl`
