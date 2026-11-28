# **Lab1实验报告**

by 20231082 吕叙鑫

## 1.思考题部分

### Think1.1

通过输入objdump --help 查看objdump相关信息如下：

可以知道参数含义为

​ -D  --disassemble-all  显示所有部分的汇编程序内容，包括所有sections.

​ -S  --source       将源代码与反汇编混合在一起，

#### 在x86环境下执行代码

```shell
gcc -E hello.c > gcc_E_hello.txt
gcc -c hello.c -o hello.o
objdump -DS hello.o > objdump_hello.txt
```

利用mips交叉编译执行代码

```shell
/OSLAB/compiler/usr/bin/mips_4KC-gcc -E hello.c -I /usr/include  >  mips_gcc_E_hello.txt
/OSLAB/compiler/usr/bin/mips_4KC-gcc -c hello.c -o hello_mips.o -I /usr/include 
/OSLAB/compiler/usr/bin/mips_4KC-objdump -DS hello_mips.o > mips_objdump_hello.txt
```

##### 结果对比为

通过对比，我们可以发现在预处理阶段，二者结果大致相同，也有一些差别。对编译后未链接结果的反汇编，由于x86指令集和mips指令集的不同，两个体系的编译器产生的反汇编结果存在很大的差异。

##### Thinking1.2

使用自己编写的readerlf和linux自带的readelf命令解析testelf和vmlinx，发现二者都可以介些testELF，但是自己编写的readelf不能解析vmlinux，而linux自带的readelf命令可以。解析testELF和vmlinux，结果如下

通过利用 readelf -h 解析testELF和vmlinux两个文件
比较发现，testELF文件是小端存储模式(little endian),vmlinux文件是大端存储模式(big endian), 而我们所编写的readelf文件采取小端存储的方式解析，不能解析大端存储的文件，所以不能解析vmlinux

##### **Thinkng 1.3**

操作系统的启动依赖bootloader来调用系统内核，从cpu上电到cpu控制权交转给操作系统内核分为两个步骤

Stage1:在ROM或者FLASH上完成，初始化相关硬件，为Stage2初始化RAM，载入Stage2到RAM，设置堆栈，并跳转到Stage2入口。

Stage2:在RAM上完成，初始化本阶段所需硬件设备，载入内核和根文件系统，为内核设置启动参数，跳转到内核入口，然后就能够将文件系统中的内核镜像文件加载到内存中，并将CPU控制权从bootloader转交给操作系统内核。

##### **Thinking 1.4**

$\mathsf{sg\_size}$  表示这个段需要的内存空间大小， $\mathsf{bin\_size}$ 表示这个段在ELF文件中的大小，由于在我们的实验中，内核的加载不一定是页对齐的，所以我们可以在一边加载一边装入内存的方法，每一次装入之后，都判断下一个加载的虚拟地址是不是和前面的装入的末尾的地址是不是在同一个页上，如果是则， 加下一个加载加载到下一页上。

##### **Thinking1.5**

linker中程序入口的设置方法有以下五种：

1. 使用ld命令时，通过参数“-e”设置
2. 在linker scirpt中使用ENTRY()指令指定了程序入口
3. 如果定义start，则start就是程序入口
4. .text段的第一个字节
5. 地址0处

在**Exercise 1.3**编写的**tools/scse0_3.lds**中我们可以发现这里采取第2种方法设置的程序入口
对内核进行反汇编来观察

可以知道从内核入口跳转到main函数，

从图中可知，内核入口在0x80010000,main函数入口的地址为0x80010040

回忆汇编知识，main函数在进行汇编之后，首地址会被翻译成标签main，通过start.S程序将栈指针指向栈顶，为main函数运行分配栈空间，然后jal main可以实现跨文件调用，跳转到main 函数地址。

跨文件调用的实现为：不同函数在汇编时函数首地址会被翻译成一个标签，而调用位置处空缺为0，然后通过链接过程将各个可重定向文件集合到一个可执行文件中，实质上是将各个段进行整合，统一分配内存空间和地址。这时候调用位置就会填入函数入口的地址，就可以跨文件调用函数了。（下图来自关于ld的课件）

##### **Thinking1.6**

```c
/* Disable interrupts */
mtc0 zero, CP0_STATUS /*将cp0_STATUS设置为0*/
......
/* disable kernel mode cache */
mfc0 t0, CP0_CONFIG // 从cp0协处理器取出CONFIG数据
and t0, ~0x7 //把$t0寄存器低3位清零
ori t0, 0x2  //把$t0中数据从低位数第二位设置为1
mtc0 t0, CP0_CONFIG //将CONFIG设置为$t0中的数据
```

查阅资料发现，将cp0_CONFIG 后三位设置为010就可以设置kseg0区不经过cache了。因为初始时，cache未初始化，不能使用。

#### 2.**实验难点图示**

lab1大致内容如上图，难点时bootloader的启动过程，这中间设计到一些硬件的初始化和软件的启动，两个步骤较为复杂。makefile的编写需要一定基础，ELF解析文件对于内存管理较为重要，熟练掌握readelf命令可以帮助我们更好解决一些问题。同时对一些程序我们需要通过反汇编来看它的汇编代码理解操作系统的一些功能。 课下实战printf函数部分大致为一个字符串解析过程，不算特别困难。课上添加读取结构体模仿其他读取方式也较为容易实现，课上的难点在于在哪里定义声明结构体，如何读取结构体变量的地址。

#### **3.体会与感想**

​ 本次实验有一定困难度，一些实验的功能实现，需要浏览多个文件，同时对于一些概念的理解有一定苦难呢。通过实验，大致了解了printf函数的实现过程，但是对于readelf的的操作不太熟悉。由于使用的gxmul工具已经提供了便利，对于操作系统进行bootloader的方式不太了解。printf在测试的时候，不会像平时用ide那样进行断点debug，通过观察汇编指令和内存数据实现debug太困难了，只能自己实际构造测试点进行测试，自己构造的数据较难以全面覆盖。希望在实验过程中可以相应提供一些测试数据来debug。

​ 实验中在解析数字时对于 a++这一个用法使用出现了错误，导致了bug。课上使用了struct结构体。操作系统用c语言来编写，需要重新拾起一些c语言的知识，温故而知新。
