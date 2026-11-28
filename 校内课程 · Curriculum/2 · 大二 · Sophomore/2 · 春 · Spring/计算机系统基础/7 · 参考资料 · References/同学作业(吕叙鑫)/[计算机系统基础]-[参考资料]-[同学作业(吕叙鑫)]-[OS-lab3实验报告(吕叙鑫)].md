# Lab3实验报告

20231082 吕叙鑫

## 1.实验思考题

### **Thinking 3.1**

**思考envid2env 函数:**

**为什么envid2env 中需要判断e->env_id != envid 的情况？如果没有这步判断会发生什么情况？**

答：

查看env_id在`mkenvid`中是如何生成的

env_id是由`asid`左移11位，第11位置1，低10位由e是`envs`数组中偏移。

而在`envid1env`函数中，当envid不为0时对envid查找是通过envid的低10位的数对应`env`数组的偏移，所以当多个进程映射到同一个虚拟地址之后，通过asid映射到不同物理地址。这些进程的虚拟地址相同，物理地址不同，生成asid时使得envid高5位不同，低10位相同，通过`e=env[ENVX(endid)]`得到的进程不一定是所需要的进程，也有可能是其他地址空间相同虚拟地址上的进程。所以需要通过`e->env_id != envid来检验。`

#### **Thinking 3.2**

**结合include/mmu.h 中的地址空间布局，思考env_setup_vm 函数：**

**• UTOP 和ULIM 的含义分别是什么，UTOP 和ULIM 之间的区域与UTOP以下的区域相比有什么区别？**

**• 请结合系统自映射机制解释Step4中pgdir[PDX(UVPT)]=env_cr3的含义。**

**• 谈谈自己对进程中物理地址和虚拟地址的理解。**

（1）

答：查看`mmu.h`中内存分布图

可以知道`UTOP=0x7f40_0000`,在该地址以下是用户能够操作的地址空间，包括 `user exception stack`（用户异常栈）`Invalid memory`不可用内存 `normal user stack`用户正常栈 。所以推断`UTOP`位用户能够操作空间地址最大值

`UTOP=0x8000_0000`在`ULIM`和`UTOP`之间为`user VPT`（用户虚拟页表空间.  `PAGES`页空间    `ENVS`（进程空间）。均为操作系统分配给用户的空间，所以推断`ULIM`为操作系统为用户分配的空间地址最大值。

（2）

`UVPT`为用户虚拟页表的地址。值为`0x7fc0_0000`，`PDX`为页目录号，所以`pgdir[PDX(UVPT)]`为寻找页目录中`UVPT`所在的页面，`env_cr3`为页目录本身所在的物理地址，所以这一代码的含义是页目录本身所在的物理地址赋值给上述页表项。

（3）

答：创建进程为我们分配一块全新的4GB的虚拟内存，同时虚拟地址与通过mmu与物理地址联系起来。进程只能操作虚拟地址，每一个进程都有自己独立的地址空间，进程切换时，不同进程对相同虚拟地址空间进行访问时互不影响，因为操作系统将它们映射到不同的物理地址。

#### **Thinking 3.3**

##### 找到 user_data 这一参数的来源，思考它的作用。没有这个参数可不可以？为什么？（可以尝试说明实际的应用场景，举一个实际的库中的例子）

答：在函数`load_icode_mapper`中，传入的`user_data`被强制转换成进程类型

推断`user_data`为指向操作进程的一个指针。

在函数`load_icode`中调用`load_icode_mapper`

在`load_elf`中，传给`load_icode_mapper` 的`user_data`即为`load_elf`中的参数`user_data`

 所以是将`load_icode`传入的`struct Env  *e`即待加载的二进制镜像的进程，赋值给`user_data`

没有这一个参数不行，因为这一参数作用是方面向更内层传参数

库函数例子有

- C语言标准库中的`qsort`函数，

`void qsort(void *base, size_t nitems, size_t size, int (*compar)(const void *, const void*))`

`base`参数可以传入任何类型的指针，`compar`参数传入的也是一个函数的指针。

#### **Thinking 3.4**

**结合load_icode_mapper 的参数以及二进制镜像的大小，考虑该函数可能会面临哪几种复制的情况？你是否都考虑到了？**

答：

需要考虑以下问题：

- va是否对齐（分对齐和没对齐两种）
- va+bin_size是否对齐（包括对齐和没对齐）
- va, va+bin_size是否在同一个页面
- va+sg_size是否对齐
- va+bin_size和va+sg_size是否在同一个页面，

考虑这些问题，进过排列组合会有以下的情况：

- va、va+bin_size、va+sg_size均不对齐切都不在同一个页面内
- Va、va+bin_size、va+sg_size均不对齐，且va,va+bin_size， va+sg_size在一个页面内
- va、va+bin_size、va+sg_size均不对齐，va,va+bin_size在一个页面内，va+sg_size在另一个页面内
- va对齐，va+bin_size, va+sg_sieze不对齐，va,va+bin_size在一个页面内，va+sg_size在另一个页面内
- ……

#### **Thinking 3.5**

**思考上面这一段话，并根据自己在lab2 中的理解，回答：**

**•** **你认为这里的 env_tf.pc 存储的是物理地址还是虚拟地址?**

**• 你觉得entry_point其值对于每个进程是否一样？该如何理解这种统一或不同？**

答：（1）`env_tf.pc`存储的是虚拟地址。一个进程的程序段的多个页面可能会分布在不同的物理地址中，对于一般程序指令执行，是`pc=pc+4`，pc值是连续变化的，而不是在分散的物理地址中来回跳转，所以推断`env_tf.pc`存储的是虚拟地址

​ （2）`entry_point`对于每一个进程来说是相同的，都是从elf文件中读取的，但是他们存储的物理地址是不同的

#### **Thinking 3.6**

 **请查阅相关资料解释，上面提到的epc是什么？为什么要将env_tf.pc设置为epc呢？**

答：`EPC`寄存器存储异常中断发生时进程正在执行的指令的地址。进行异常处理的时候，进程上下文的`env_tf.pc`应该设置为`epc`，使得中断处理完之后返回该进程时能够返回到发生中断的地方继续执行进程。

#### **Thinking 3.7**

**关于 TIMESTACK，请思考以下问题：**

##### • 操作系统在何时将什么内容存到了 TIMESTACK 区域

##### • TIMESTACK 和 env_asm.S 中所定义的 KERNEL_SP 的含义有何不同

答（1）

查看mmu中关于`TIMESTACK`的定义

```c
#define TIMESTACK 0x82000000
```

在`include/stackframe.h`中找到如下代码

```assembly
.macro get_sp
 mfc0 k1, CP0_CAUSE #读CP0_cause寄存器到$k1
 andi k1, 0x107C  #取k1的第2-6、13位
 xori k1, 0x1000  
 bnez k1, 1f   #判断是否位时钟中断
 nop
 li sp, 0x82000000 #如果是时钟中断，设置sp为TIMESTACK用于保存上下文
 j 2f
 nop
1: #不是时钟中断跳转到这里
 bltz sp, 2f #sp寄存器小于0，跳转到2
 nop
 lw sp, KERNEL_SP #将sp寄存器的值写入KERNEL_SP
 nop

2: #是时钟中断，跳转到这里
 nop
.endm
```

在进行进程切换时保存寄存器的值

从使用以及命名推断`TIMESTACK`为发生时钟中断时存放寄存器状态的栈顶地址。在发生时钟中断进行进程切换时，将寄存器的值保存在`TIMESTACK`对应的页面。
（2）

答：从`include/stackfram.h`中的`get_sp`函数发现，发生时钟中断时向sp寄存器存入`TIMESTACK`这一个地址，将进程的寄存器状态保存到TIMESTACK对应的页面中。不为时间中断，向sp寄存器存入`KERNEL_SP`指向的地址，将寄存器状态保存到这一个地址中。

#### **Thinking 3.8**

**试找出上述 5 个异常处理函数的具体实现位置。**

**0 号异常**的处理函数为`handle_int`，表示中断，由时钟中断、控制台中断等中断造成

**1 号异常**的处理函数为`handle_mod`，表示存储异常，进行存储操作时该页被标记为只读

**2 号异常**的处理函数为`handle_tlb`，TLB 异常，TLB 中没有和程序地址匹配的有效入口

**3 号异常**的处理函数为`handle_tlb`，TLB 异常，TLB 失效，且未处于异常模式（用于提高处理效率）

**8 号异常**的处理函数为`handle_sys`，系统调用，陷入内核，执行了 syscall 指令

`handle_int` 、`handle_mod`和`handle_tlb`具体实现在`lib/genex.S`中，`handle_sys`在`lib/syscall.S`中

`handle_int`：

```assembly
NESTED(handle_int, TF_SIZE, sp)
.set noat
nop

SAVE_ALL
CLI
.set at
mfc0 t0, CP0_CAUSE
mfc0 t2, CP0_STATUS
and t0, t2

andi t1, t0, STATUSF_IP4
bnez t1, timer_irq
nop
END(handle_int)

timer_irq:
 sb zero, 0xb5000110
1: j sched_yield
 nop
 /*li t1, 0xff
 lw    t0, delay
 addu  t0, 1
 sw t0, delay
 beq t0,t1,1f 
 nop*/
 j ret_from_exception
 nop
```

`handle_tlb`和`handle_mod`：

```assembly
BUILD_HANDLER reserved do_reserved cli
BUILD_HANDLER tlb do_refill cli
BUILD_HANDLER mod page_fault_handler cli

NESTED(do_refill,0 , sp)
   //li k1, '?'
   //sb k1, 0x90000000
   .extern mCONTEXT
//this "1" is important
1:   //j 1b
   nop
   lw  k1,mCONTEXT
   and  k1,0xfffff000
    mfc0  k0,CP0_BADVADDR
    srl  k0,20
    and  k0,0xfffffffc
   addu  k0,k1
   
   lw  k1,0(k0)
   nop
     move  t0,k1
     and  t0,0x0200
     beqz  t0,NOPAGE
   nop
   and  k1,0xfffff000
    mfc0  k0,CP0_BADVADDR
    srl  k0,10
    and  k0,0xfffffffc
    and  k0,0x00000fff
   addu  k0,k1

   or  k0,0x80000000
   lw  k1,0(k0)
   nop
     move  t0,k1
     and  t0,0x0200
     beqz  t0,NOPAGE
   nop
   move  k0,k1
   and  k0,0x1
   beqz  k0,NoCOW
   nop
   and  k1,0xfffffbff
NoCOW:
   mtc0  k1,CP0_ENTRYLO0
   nop
   tlbwr
   j  2f
   nop
NOPAGE:
//3: j 3b
nop
   mfc0  a0,CP0_BADVADDR
   lw  a1,mCONTEXT
   nop
    
   sw   ra,tlbra
   jal  pageout
   nop
//3: j 3b
nop
   lw  ra,tlbra
   nop
   j 1b
2:   nop
   jr  ra
   nop
END(do_refill)
```

`handle_sys`:

```assembly
NESTED(handle_sys,TF_SIZE, sp)

SAVE_ALL
CLI

//1: j 1b
nop
.set at
lw t1, TF_EPC(sp)
sw      t1, TF_EPC(sp)
la      t1, sys_call_table
lw      t2, (t1)
lw      t0,TF_REG29(sp)

lw      t1, (t0)
lw      t3, 4(t0)
lw      t4, 8(t0)
lw      t5, 12(t0)
lw      t6, 16(t0)
lw      t7, 20(t0)

subu    sp, 20

sw      t1, 0(sp)
sw      t3, 4(sp)
sw      t4, 8(sp)
sw      t5, 12(sp)
sw      t6, 16(sp)
sw      t7, 20(sp)

move    a0, t1
move    a1, t3
move    a2, t4
move    a3, t5

jalr    t2
nop

addu    sp, 20

sw      v0, TF_REG2(sp)

j       ret_from_exception//extern?
nop

illegal_syscall: j illegal_syscall
   nop
END(handle_sys)
```

#### Thinking 3.9

##### 阅读 kclock_asm.S 和 genex.S 两个文件，并尝试说出 set_timer 和time_irq 函数中每行汇编代码的作用

答：`lib/klock_asm.S`，`set_timer`实现如下：

```assembly
LEAF(set_timer)
 li t0, 0xc8 #将t0寄存器储存0xc8,表示时钟频率，一秒钟中断200次
 sb t0, 0xb5000100 #将t0寄存器的值写入到地址为0xb500_0100中，0xb500_0000是gxemul映射实时钟的位置，偏移量为0x100位置用来设置实时钟中断的频率
 sw sp, KERNEL_SP #将sp寄存器中的值存到KERNEL_SP
 setup_c0_status STATUS_CU0|0x1001 0  #调用函数setup_c0_status设置cp0_STATUS的值
 jr ra 
 nop
END(set_timer)
```

在`lib/genex.S`中，`timer_irq`实现为：

```assembly
timer_irq:

 sb zero, 0xb5000110 #关闭实时钟
1: j sched_yield 跳转到调度函数
 nop
 /*li t1, 0xff
 lw    t0, delay
 addu  t0, 1
 sw t0, delay
 beq t0,t1,1f 
 nop*/
 j ret_from_exception #从异常处理程序汇总返回
 nop
```

#### Thinking 3.10

**阅读相关代码，思考操作系统是怎么根据时钟周期切换进程的。**

答：

在我们实现的操作系统中，是采用时间片轮转算法，每一个进程被分到一个时间片，用作计时。设置一个进程就绪队列`env_shed_list`。每当一个进程的时间片用完是，代表该进程需要进行时钟中断，进程切换。如果该进程还没有结束，则移到队列尾部，时间片复原，从就绪队列头部取出一个进程直到该进程结束或者时间片用完，如此往复循环。 我们的实验的`env_shed_list`数组有两个，表示两个进程队列，在取出队列中的进程时进程不一定是就绪进程，需要进行判断。同时将env_pri用作分配的时间片，并在系统获取到该进程时，将`env_pri`赋值给`count`,每运行一次`count`减去1，代表时间片用了一段。当`count`减为0时表示该进程时间片已经用完，将这个进程移到另一个进程队列的尾部。如果这个进程队列没有进程了则转到另一个进程队列直到另一个进程列表为空。

## 2.实验难点图示

## 3.体会与感受

实验还是一如既往的难。实验量较大，需要明白进程的整个生命周期以及控制块的作用。同时对于二进制文件加载，了解加载的过程以及，加载方式的对齐十分重要。对于进程的虚拟地址空间分配，以及在进程切换时进行的处理理解还不是很透彻，对于协处理器CP0寄存器的使用没有深入的了解，基本上是按照教程的步骤完成代码。对于进程调度方式，需要考虑一些边界条件。总之，实验还好，课上实验在课下的基础上勉强算是通过了。

## 4.指导书反馈

进程调度时，进程时间片用完后，指导书写的插入头部，而代码则提示插入尾部;
