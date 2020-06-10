- jffs

    ```python

    sudo apt-get install mtd-tools
    Load kernel modules (note that you can adjust the size of the mtd device while loading mtdram):

    sudo modprobe mtd
    sudo modprobe jffs2
    sudo modprobe mtdram total_size=16384 erase_size=512
    sudo modprobe mtdchar (이건 없는거 같다.)
    sudo modprobe mtdblock
    Load jffs2 image into mtd block device:

    sudo dd if=firmware.jffs2 of=/dev/mtd0
    (firmware.jffs2 : 마운트할 이미지이름)
    You are now ready to mount the image:

    sudo mkdir /mnt/image
    sudo mount -t jffs2 /dev/mtdblock0 /mnt/image

    ```

- squashfs mount 시키기

    ```python
    ### mksquashfs
    $ mksquashfs new_second.bin -comp xz

    ### unsquashfs ...
    $ mkdir ./mount_squashfs
    $ mount -t squashfs -o loop sqsh.img ./mount_squashfs

    ### unmount 
    umount -l DIRECTORY 
    umount -f DIRECTORY  (-f:force) 
    ```

- squashfs 수정하기

    ```python
    sudo apt-get install squashfs-tools
    unsquashfs target.squashfs
    cd squashfs
    ### 수정 
    cd ../
    mksquashfs squashfs new-squashfs  
    mksquashfs squashfs new-squashfs -comp xz ## 최대로 압축을 해야하는 경우 
    ```

- jffs2 수정하기

    ```python
    sudo modprobe mtdblock
    sudo mpdprobe mtdram total_size=0x....
    sudo dd if=./target.jffs2 of=/dev/mtdblock0
    sudo mount -t jffs2 /dev/mtdblock0 ./jffs2/
    sudo dd if=/dev/mtdblock0 of =./newjffs2
    ```
