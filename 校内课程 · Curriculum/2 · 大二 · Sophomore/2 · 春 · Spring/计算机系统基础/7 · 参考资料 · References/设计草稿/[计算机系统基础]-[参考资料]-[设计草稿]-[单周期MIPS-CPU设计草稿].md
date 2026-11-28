# Logisim · draft

## 设计草稿

本草稿为单周期MIPS架构下的CPU设计方案，包含IFU, GRF, NPC, ALU, CU(Contro Unit)，DM等模块，目前可以实现add, sub, ori, lw, sw, beq, lui共7条指令。以下为各模块定义及详细信息。

### IFU

| 信号名 | 方向 | 位宽 | 描述 |
| --- | --- | --- | --- |
| clk | I | 1 | 时钟信号 |
| reset | I | 1 | 异步复位信号 |
| nextPC | I | 32 | 下一条指令的地址 |
| curPC | O | 32 | 当前指令的地址 |
| Instr. | O | 32 | 当前指令 |

内部包含32位PC寄存器以及32位ROM作为指令寄存器（IM）。对MARS中指令地址从`0x0000_3000`进行了特殊处理，对输入信号`NextPC`减去`0x0000_3000`再存入寄存器；而ROM的读取地址则直接与寄存器读出端相连，在提供给`curPC`端口前再加上`0x0000_3000`。该处理与异步复位兼容。

### GRF

| 信号名 | 方向 | 位宽 | 描述 |
| --- | --- | --- | --- |
| clk | I | 1 | 时钟信号 |
| reset | I | 1 | 异步复位信号 |
| A1 | I | 32 | 读寄存器的地址，读出至RD1 |
| A2 | I | 32 | 读寄存器的地址，读出至RD2 |
| A3 | I | 32 | 写寄存器的地址 |
| WE | I | 1 | 写入使能信号，当前仅当为1时写入有效 |
| WD | I | 32 | 写入数据 |
| RD1 | O | 32 | A1指定的寄存器的数据 |
| RD2 | O | 32 | A2指定的寄存器的数据 |

共包含32个寄存器，分别对应MIPS架构中的`$0`至`$31`通用寄存器。其中，`$0`恒为0，无法写入其他数据；其余寄存器在写入使能信号为1时允许写入地址对应的寄存器被写入。

### NPC

| 信号名 | 方向 | 位宽 | 描述 |
| --- | --- | --- | --- |
| curPC | I | 32 | 当前指令的地址 |
| Imm_16 | I | 16 | B类指令地址偏移量（未扩展为32位） |
| Instr.26 | I | 26 | J类指令跳转index |
| branch | I | 1 | B类指令跳转信号 |
| jr | I | 1 | jr指令跳转新号，当且仅当为1时满足跳转条件 |
| jump | I | 1 | J类指令跳转信号 |
| ra | I | 32 | `$ra`寄存器的值 |
| nextPC | O | 32 | 下一条指令的地址 |
| +4PC | O | 32 | 将下一指令地址传出，适配jal指令 |

无跳转时固定执行将`curPC + 4`传入`nextPC`端口。需要跳转时在内部进行判断，进行其他处理。对Imm_16的符号扩展在本模块内部进行而非通过EXT模块进行，相应地，CU中相关的B类指令就可以不指定SignedEXT。

### ALU

| 信号名 | 方向 | 位宽 | 描述 |
| --- | --- | --- | --- |
| A | I | 32 | 运算数1 |
| B | I | 32 | 运算数2 |
| ALUOp | I | 4 | 功能选择信号，详见下方 |
| Shamt | I | 32 | 移位数 |
| Result | O | 32 | 运算结果 |
| Equals | O | 1 | 判断相等信号 |

---

#### ALUOp设置

| ALUOp | Result |
| --- | --- |
| 0000 | A + B |
| 0001 | A - B |
| 0010 | A AND B |
| 0011 | A OR B |
| 0100 | A XOR B |
| 0101 | A NOR B |
| 0110 | A << B |
| 0111 | A >> B |
| 1000 | A >>> B |
| 1001 | `$signed(A) > $signed(B)` |
| 1010 | A > B |

逻辑运算单元，具有加、减、按位与、按位或等多种功能（详见上方表格），根据`ALUOp`进行功能选择，输出至`Result`。`Equals`端口用于特殊判定是否触发`beq`。

### DM

| 信号名 | 方向 | 位宽 | 描述 |
| --- | --- | --- | --- |
| clk | I | 1 | 时钟信号 |
| reset | I | 1 | 异步复位信号 |
| Addr | I | 16 | 写入地址 |
| Data | I | 32 | 写入数据 |
| MemWrite | I | 1 | 写入使能信号，当前仅当为1时写入有效 |
| RD | O | 32 | Addr指定的存储单元的数据 |

内部包含32位RAM作为存储器，支持写入和读出数据。目前仅支持完整的字操作（即`sw`和`lw`命令），尚不支持对字节/半字进行操作。

### BP

| 信号名 | 方向 | 位宽 | 描述 |
| --- | --- | --- | --- |
| A | I | 32 | 参与判断的寄存器值 |
| BranchOp | I | 4 | 判断条件选择信号，详见下方 |
| Equals | I | 1 | 相等信号 |
| Result | O | 1 | 是否跳转 |

---

#### BranchOp设置

| BranchOp | 对应指令 | CheckIf |
| --- | --- | --- |
| 0000 | beq | Equals |
| 0001 | blez | A < 0 |
| 0010 | bne | not Equals |
| 0011 | | |
| 0100 | | |
| 0101 | | |
| 0110 | | |
| 0111 | | |
| 1000 | | |
| 1001 | | |
| 1010 | | |

BP模块用于判断B类指令是否跳转并将信号传递给nPC。在变量命名方面，为与CU部分的Branch信号（是否检测到当前指令为B类指令）做区分，使用小写b的branch信号作为输出。其中，因为beq和bne涉及<span style="color :red;">两个</span>寄存器值相互比较，可以在ALU模块中完成，而不用单独为之在BP中增加输入端口。

### CU

| | RegDst | Mem2Reg | MemWrite | RegWrite | ALUSrc | ALUOp | SignedExt | Branch | jr | Jump | BranchOp | link |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **add** | 1 | 0 | 0 | 1 | 0 | 0000 | X | 0 | 0 | 0 | X | 0 |
| **sub** | 1 | 0 | 0 | 1 | 0 | 0001 | X | 0 | 0 | 0 | X | 0 |
| **ori** | 0 | 0 | 0 | 1 | 1 | 0011 | 0 | 0 | 0 | 0 | X | 0 |
| **lw** | 0 | 1 | 0 | 1 | 1 | 0000 | 1 | 0 | 0 | 0 | X | 0 |
| **sw** | X | X | 1 | 0 | 1 | 0000 | 1 | 0 | 0 | 0 | X | 0 |
| **lui** | 0 | 0 | 0 | 1 | 1 | 0110 | 0 | 0 | 0 | 0 | X | 0 |
| **and** | 1 | 0 | 0 | 1 | 0 | 0010 | X | 0 | 0 | 0 | X | 0 |
| **sll** | 1 | 0 | 0 | 1 | 0 | 0110 | X | 0 | 0 | 0 | X | 0 |
| **jr** | X | X | 0 | 0 | X | X | X | 0 | 1 | 0 | X | 0 |
| **beq** | X | X | 0 | 0 | 0 | X | X | 1 | 0 | 0 | 0000 | 0 |
| **blez** | X | X | 0 | 0 | X | X | X | 1 | 0 | 0 | 0001 | 0 |
| **j** | X | X | 0 | 0 | X | X | X | 0 | 0 | 1 | X | 0 |
| **jal** | X | X | 0 | 1 | X | X | X | 0 | 0 | 1 | X | 1 |

按照教程，对`CU`进行了和逻辑和或逻辑的拆分，内部为各指令创建控制信号。这一设计模式便于添加指令和debug。

### 数据通路

| | nPC | IFU | GRF | | | | EXT | ALU | | | DM | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | curPC | nextPC | A1 | A2 | A3 | WD | Imm16 | A | B | Shamt | Addr | Data |
| add | IFU.curPC | nPC.nextPC | IFU.Instr.[25:21] | IFU.Instr.[20:16] | IFU.Instr.[15:11] | ALU.Result | | GRF.RD1 | GRF.RD2 | | | |
| sub | IFU.curPC | nPC.nextPC | IFU.Instr.[25:21] | IFU.Instr.[20:16] | IFU.Instr.[15:11] | ALU.Result | | GRF.RD1 | GRF.RD2 | | | |
| ori | IFU.curPC | nPC.nextPC | IFU.Instr.[25:21] | | IFU.Instr.[20:16] | ALU.Result | IFU.Instr.[15:0] | GRF.RD1 | EXT.Imm_32 | | | |
| lw | IFU.curPC | nPC.nextPC | IFU.Instr.[25:21] | | IFU.Instr.[20:16] | DM.RD | IFU.Instr.[15:0] | GRF.RD1 | EXT.Imm_32 | | ALU.Result | |
| sw | IFU.curPC | nPC.nextPC | IFU.Instr.[25:21] | IFU.Instr.[20:16] | | | IFU.Instr.[15:0] | GRF.RD1 | EXT.Imm_32 | | ALU.Result | GRF.RD2 |
| beq | IFU.curPC | nPC.nextPC | IFU.Instr.[25:21] | IFU.Instr.[20:16] | | | | GRF.RD1 | GRF.RD2 | | | |
| blez | FU.curPC | nPC.nextPC | IFU.Instr.[25:21] | | | | | | | | | |
| lui | IFU.curPC | nPC.nextPC | IFU.Instr.[25:21] | | IFU.Instr.[20:16] | ALU.Result | IFU.Instr.[15:0] | | GRF.RD2 | CU.Shamt | | |
| and | IFU.curPC | nPC.nextPC | IFU.Instr.[25:21] | IFU.Instr.[20:16] | IFU.Instr.[15:11] | ALU.Result | | GRF.RD1 | GRF.RD2 | | | |
| sll | IFU.curPC | nPC.nextPC | | IFU.Instr.[20:16] | IFU.Instr.[15:11] | ALU.Result | | | GRF.RD2 | CU.Shamt | | |
| jr | IFU.curPC | nPC.nextPC | IFU.Instr.[25:21] | | | | | | | | | |
| j | IFU.curPC | nPC.nextPC | | | | | | | | | | |
| jal | IFU.curPC | nPC.nextPC | | | 常量0x1f | nPC.+4PC | | | | | | |

严格按照各模块端口名称，列出数据通路。

---

### 待办

- [x] 添加b类和j类指令跳转，为B类移除`branch`改为`BranchOp`，为J类添加`Jump`
- [x] 移除nPC模块的`equals`，将`Branch`统一定义为所有B类跳转指令的跳转信号
- [x] 为jal添加数据通路控制信号`link`，分别控制写入数据来源和写入地址选择
- [ ] 整合RegDst和Link涉及的数据选择信号
- [ ] 测试ALU部分涉及符号的处理是否得当
- [x] MIPS_generator生成数据逻辑用draw.io绘图给zyt看
- [x] MIPS_generator补充jal与jr对应部分
- [x] 命令行运行MARS的输出重定向
- [ ] 增加某些寄存器生成概率，有目的性地测试【提高找到bug的概率】
- [x] 命令行运行MARS如何默认关闭arithmetic overflow检测
- [ ] 运行错误检测：二次删改代码
- [x] win版ISE
- [x] pipeline.py中调用os，命令行执行
- [ ] 迁移P4至CPUTester文件夹并测试
- [ ] pipline.py中完成忽略指令的功能

## 测试方案

前期使用手搓数据+用评论区其他同学提供的对比程序进行比对。后期使用了舍友编写的数据生成程序，增加测试强度。发现跳转指令会产生死锁，存取指令在纯随机条件下无法保证地址是整字，对此做出了一定调整，详见下方。

### 计算指令

```verilog
# use ori to initiate
# some randomly generated numbers
ori $0, $0, 42  
ori $1, $0, 17  
ori $2, $0, 99  
ori $3, $0, 8  
ori $4, $0, 1  
ori $5, $0, 2  
ori $6, $0, 88  
ori $7, $0, 54  
ori $8, $0, 31  
ori $9, $0, 76  
ori $10, $0, 12  
ori $11, $0, 5  
ori $12, $0, 101  
ori $13, $0, 23  
ori $14, $0, 37  
ori $15, $0, 90  
ori $16, $0, 14  
ori $17, $0, 67  
ori $18, $0, 3  
ori $19, $0, 74  
ori $20, $0, 58  
ori $21, $0, 29  
ori $22, $0, 84  
ori $23, $0, 11  
ori $24, $0, 23   
ori $25, $0, 887  
ori $26, $0, 2  
ori $27, $0, 0  
ori $28, $0, 10778  
 
add $24, $27, $27  # $24 = 0 + 0  
add $25, $27, $1   # $25 = 0 + 17 
add $26, $27, $2   # $26 = 0 + 99  
add $27, $27, $3   # $27 = 0 + 8  
 
sub $24, $0, $4    # $24 = 0 - 1  
sub $25, $0, $5    # $25 = 0 - 2  
sub $26, $0, $0    # $26 = 0 - 0   

# covering numbers located at the edge of 16-digit range
ori $28, $0, 11777 # $28 = 11777  
ori $29, $0, 65534 # $29 = 65534  
ori $30, $0, 65535 # $30 = 65535  
 
ori $21, $0, 25779 # $21 = 25779  
ori $22, $0, 42528 # $22 = 42528  
ori $23, $0, 34567 # $23 = 34567
 
sub $24, $0, $28    # $24 = 0 - 65533 
sub $25, $0, $29    # $25 = 0 - 65534 

ori $31, $0, 0     # $31 = 0  
# testing whether it is able to write $0
add $0, $0, $1     # $0 = 0 + 1  
add $1, $21, $23   # $1 = 25779 + 34567
add $2, $28, $22    # $2 = 11777 + 42528
```

本样例从简单、小规模随机数启动，逐渐覆盖大数和边界情况，充分测试了`add`和`sub`命令。对于`ori`和`lui`更高强度的测试将在**跳转指令**和**访存指令**中作为初始化语句一并进行。

### 跳转指令

```verilog
# use lui and ori to initiate
lui $t0, 0x0001      
ori $t0, $t0, 0x0001  

lui $t1, 0x0002       
ori $t1, $t1, 0x0002 

lui $t2, 0x0003 
ori $t2, $t2, 0x0003 

lui $t3, 0x0001 
ori $t3, $t3, 0x0001 

lui $t4, 0x0003 
ori $t4, $t4, 0x0003 

# unsatified jump
unsatified_backward:
beq $t0, $t1, unsatified_forward
beq $t0, $t2, unsatified_backward
unsatified_this:
beq $t1, $t2, unsatified_this

# successful jump
beq $t0, $t3, jump_forward
jump_backward:
beq $t1, $t3, jump_forward2

jump_forward:
lui $t1, 0x0001  
ori $t1, $t1, 0x0001
beq $t1, $t0, jump_backward

jump_forward2:
lui $t5, 0x0034  
ori $t5, $t5, 0x0034

beq $t2, $t4, jump_next
jump_next:

jump_this:
beq $t2, $t4, jump_this

unsatified_forward:
```

通过本样例，充分测试跳转成功与失败的情况，覆盖向前、向后和原地的跳转。其中，向后跳转（即`offset为负`）的情况帮助我de出了一处bug：我使用教程中在`nPC`内处理`offset`扩展的方法，但是使用了零扩展，导致`offset`为负时扩展后变一个巨大的正数，错误改变了`PC`。

在数据生成时，遇到了死循环情况。经过分析，决定在每个`offset`为负的跳转语句（假设从A跳回至B）前增加一个跳转区域，跳转区域的有一指令是跳转至A之后。同时使第一次在执行B之前就跳入跳转区域，保证了不会出现死循环。典型MIPS代码见下方：

```verilog

ori $2, $25, 15340
beq $0, $0, label15   #进入跳转区域
label16:              #B: 跳回标签
sub $25, $5, $2
beq $0, $0, label14   #跳转区域内，跳至A之后
label15:              #进入跳转区域时，要在离开跳转区域的指令之后
add $11, $14, $10
beq $3, $7, label16   #A: offset为负的beq
label14:
nop
add $16, $22, $13
```

### 访存指令

```verilog
# initiate
ori $t0, $0, 0         # $t0 = 0x00000000  
ori $t1, $0, 1         # $t1 = 0x00000001  
lui $t2, 0xFFFF         
ori $t2, $t2, 0xFFFF   # $t2 = 0xFFFFFFFF  
lui $t3, 0x7FFF       
ori $t3, $t3, 0xFFFF   # $t3 = 0x7FFFFFFF  
lui $t4, 0x7FFF          
ori $t4, $t4, 0xFFFE   # $t4 = 0x7FFFFFFE  
lui $t5, 0x8000        # $t5 = 0x80000000  
lui $t6, 0x8000          
ori $t6, $t6, 0x0001   # $t6 = 0x80000001   
ori $t7, $t7, 0xFFFF   # $t7 = 0x0000FFFF  
lui $t8, 0x0000    
ori $t8, $t8, 0xFFFE   # $t8 = 0x0000FFFE  
  
sw $t0, 0($0)  
sw $t1, 4($0)  
 
ori $t9, $0, 12  
sw $t2, 0($t9)  
 
ori $a1, $0, 16   
sw $t3, -4($a1)     
  
sub $t7, $0, $a1
sw $t4, 20($t7)         
 
sw $t6, 12($a1)   

lw $t6, 0($0)  
lw $t5, 4($0)  
lw $t4, 0($t9) 
lw $t3, -4($t9)   
 
sub $9, $0, $t9    
lw $t1, 16($t9)    
 
add $9, $0, $t9  
lw $0, -8($9)   
```

测试访存指令需要考虑`$base`和`offset`的多种正负情况，已在样例中进行覆盖。此外，特别判断了`$0`是否可以被写入。

## 思考题

1. 上面我们介绍了通过 FSM 理解单周期 CPU 的基本方法。请大家指出单周期 CPU 所用到的模块中，哪些发挥状态存储功能，哪些发挥状态转移功能。

   - 状态存储功能：PC（程序计数器）、IM（指令存储器）、GRF（寄存器堆）、DM（数据存储器）
   - 状态转移功能：Splitter、Controller、ALU、EXT、MUX、全加器（改变PC）

2. 现在我们的模块中 IM 使用 ROM， DM 使用 RAM， GRF 使用 Register，这种做法合理吗？ 请给出分析，若有改进意见也请一并给出。

   IM使用ROM似乎并不太合适，只读存储器的特点限制了CPU在运行中不断增加新指令的可能，降低了使用灵活性。可以考虑改用可编程类型的只读存储器。

   DM使用RAM和GRF使用Register的操作比较合理，其中RAM支持读写的能力保证了数据的存取，而Register的高速访问特性保证了CPU运行速度。

3. 在上述提示的模块之外，你是否在实际实现时设计了其他的模块？如果是的话，请给出介绍和设计的思路。

   无。

4. 事实上，实现 `nop` 空指令，我们并不需要将它加入控制信号真值表，为什么？

   `nop`指令等价于`sll $0, $0, 0`，指令码为`0x0000_0000`，不会触发其他指令，因此无任何其他操作。

5. 阅读 Pre 的 [“MIPS 指令集及汇编语言”](http://cscore.buaa.edu.cn/tutorial/mips/mips-6/mips6-1/) 一节中给出的测试样例，评价其强度（可从各个指令的覆盖情况，单一指令各种行为的覆盖情况等方面分析），并指出具体的不足之处。

   测试样例覆盖了现阶段需要的指令，但是单一指令的测试面较低。

   1. `add`和`sub`并未测试16位数边界处的情况。
   2. `lui`测试了符号位的情况，但`ori`缺少对大数和范围内随机数的覆盖。
   3. `beq`测试较简单，没有测试`offset`正负零的多种情况。
   4. `sw`和`lw`并未测试`$base`为正负的情况，`offset`为负的情况也未覆盖

   总体来说，强度不足。

---

1. 在相应的部件中，复位信号的设计都是**同步复位**，这与 P3 中的设计要求不同。请对比**同步复位**与**异步复位**这两种方式的 reset 信号与 clk 信号优先级的关系。
   - 在同步复位中，`clk`的优先级高于`reset`的优先级。
   - 在同步复位中，`reset`的优先级高于`clk`的优先级。
2. C 语言是一种弱类型程序设计语言。C 语言中不对计算结果溢出进行处理，这意味着 C 语言要求程序员必须很清楚计算结果是否会导致溢出。因此，如果仅仅支持 C 语言，MIPS 指令的所有计算指令均可以忽略溢出。 请说明为什么在忽略溢出的前提下，addi 与 addiu 是等价的，add 与 addu 是等价的。

​

## 特别注意

- [x] MARS 中的指令地址是从`0x0000_3000`开始的，而导入ROM后地址从`0`开始，要对其做一些处理才可以使CPU正常运转
- [ ] debug时更改了GRF的WD线上的MUX特性，设置“Disabled Output”为Zero。当时不确定是否会造成影响，如果上机出现问题可以调整。
