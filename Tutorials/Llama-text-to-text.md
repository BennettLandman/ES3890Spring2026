# Get a GPU Node on ACCRE

**[<VUID>@gw01 ~]$ salloc --time=120:00 --account=es3890_acc --partition=batch_gpu --gres=gpu:nvidia_rtx_a6000:1**

**salloc: Pending job allocation 8755947**

**salloc: job 8755947 queued and waiting for resources**

**salloc: job 8755947 has been allocated resources**

**salloc: Granted job allocation 8755947**

**salloc: Waiting for resource configuration**

**salloc: Nodes gpu#### are ready for job**

# Create a tunnet from localhost

Replace gpu#### with the response from above. 

~ % ssh -L2222:gpu####:22 `<vuid>@login.accre.vu`

# Use the tunnel to connect

**~ % ssh -p 2222 localhost**

**Authorized uses only. All activity may be monitored and reported. Vanderbilt University - Advanced Computing Center for Research & Education**

**GPU Node - x86_64v4**

**[<VUID>@gpu0059 ~]$**

# Optional: Use ssh hosts in VS Code to work locally
