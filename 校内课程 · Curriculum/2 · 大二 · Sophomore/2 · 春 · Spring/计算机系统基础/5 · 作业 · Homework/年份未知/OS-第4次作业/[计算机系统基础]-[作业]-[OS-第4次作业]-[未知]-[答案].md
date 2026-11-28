# 计算机系统基础 OS-第4次作业答案（年份未知）

## 1

### 题目

三个进程 P1、P2、P3 互斥使用一个包含 $N$（ $N>0$）个单元的缓冲区。P1 每次用 produce() 生成一个正整数并用 put() 送入缓冲区某一个空单元中；P2 每次用 getodd() 从该缓冲区中取出一个奇数并用 countodd() 统计奇数个数；P3 每次用 geteven() 从该缓冲区中取出一个偶数并用 counteven() 统计偶数个数。请用信号量机制实现这三个进程的同步与互斥活动，并说明所定义的信号量的含义。

### 答案

**答案：**

答：

 三个进程共享缓冲区，对缓冲区需要添加信息量进行保护，为mutex，且初值为1；

 缓冲区中空位的个数为三个进程共享，设信息量为empty，初始值为N。

 P1和P2共享缓冲区中奇数的个数，奇数的个数需要信息量，设为odd，初值为0；P1和P3共享缓冲区中的偶数个数，记偶数的个数信息量为even，初值为1。

```c
Semaphore mutex = 1, odd = 0, even = 1,empty = N

P1:
while(true) {
  P(empty);
      integer = produce();
  P(mutex);
      put();
        if (integer %2 == 0) {
        V(even)
      } else {
        V(odd)
      }
  V(mutex)

}

P2:
while(true) {
  P(odd);
  P(mutex);
      getodd();
  V(mutex);
  V(empty);
  countodd();
}

P3:
while(true) {
  P(mutex);
    P(even);
      geteven();
  V(mutex);
  V(empty);
  counteven();
}
```

## 2

一个野人部落从一个大锅中一起吃炖肉，这个大锅一次可以存放 $M$ 人份的炖肉。当野人们想吃的时候，如果锅中不空，他们就自助着从大锅中吃肉。如果大锅空了，他们就叫醒厨师，等待厨师再做一锅肉。

野人线程未同步的代码如下：

```c
while (true) {
    getServingFromPot();
    eat();
}
```

厨师线程未同步的代码如下：

```c
while (true) {
    putServingsInPot(M);
}
```

同步的要求是：

- 当大锅空的时候，野人不能够调用 getServingFromPot()。
- 仅当大锅为空的时候，大厨才能够调用 putServingsInPot()。

### 题目

问题：请写出使用 PV 满足同步要求的完整程序。

### 答案

**答案：**

 野人线程未同步的代码如下:

```C
while (true){
    getServingFromPot();
    eat();
}
```

 厨师线程未同步的代码如下:

```C
 while (true) {
     putServingsInPot(M);
}
```

同步的要求是: 当大锅空的时候，野人不能够调用 getServingFromPot() 仅当大锅为空的时候，大厨才能够调用 putServingsInPot()

问题:请写出使用 PV 满足同步要求的完整程序。

 设置信号量empty=1表示没有食物，野人等待，设置Have=1表示有食物，厨师等待，设置肉的数量为food=0；

```text
Semaphore

savages:
while(true){
    P(Have);
    getServingFromPot();
    food--;
    if (food == 0)
        V(empty);
    else {
        V(Have);
    }
    eat();
}

cook:
while(true) {
    P(empty);
        putServingsInPot(M);
        food += M;
    V(Have);
}
```

## 3

### 题目

系统中有多个生产者进程和消费者进程，共享用一个可以存 1000 个产品的缓冲区（初始为空），当缓冲区为未满时，生产者进程可以放入一件其生产的产品，否则等待；当缓冲区为未空时，消费者进程可以取走一件产品，否则等待。要求一个消费者进程从缓冲区连续取出 10 件产品后，其他消费者进程才可以取产品，请用信号量 P、V 操作实现进程间的互斥和同步，要求写出完整的过程；并指出所用信号量的含义和初值。

### 答案

**答案：**

 mutex表示是否占用缓冲区，empty表示缓冲区空余未知的个数，初始empty=1000；ProductNum表示缓冲区产品数量，初始为0；NoConsumer表示缓冲区中没有消费者，初始为1

```C
Semaphore mutex = 1, empty = 1000, ProductNum = 0, NoConsumer = 1;

Producer:
while(true) {
    p(empty);
    p(mutex);
        produce();
    V(mutex);
    V(ProductNum);
}

Consumer:
while(true) {
    P(NoConsumer);
    for (int i = 0; i < 10; i++) {
        P(ProductNum);
        P(mutex);
            consume();
        V(mutex);
        V(empty);
    }
    V(NoConsumer);
}
```

## 4

### 题目

读者写者问题的写者优先算法：

1. 共享读；
2. 互斥写、读写互斥；
3. 写者优先于读者（一旦有写者，则后续读者必须等待，唤醒时优先考虑写者）。

### 答案

**答案：**

```C
Semaphore write_write = 1;    //保证写-写互斥
Semaphore read_write = 1;    //保证读-写之间互斥
Semaphore writers_mutex;    //保证访问共享变量写者互斥
Semaphore readers_mutex;    //保证访问共享变量读者互斥
Semaphore no_writer = 1;    //保证写者优先
int writers = 0, readers = 0;    //记录写者读者数量

Reader:
while(true) {
    P(no_writer);
      P(read_write);
      P(readers_mutex);
          readers++;
          if(readers == 1)
            P(write_write);
    V(readers_mutex);
    V(read_write);
    V(no_writer);
    read();
    P(readers_mutex);
        readers--;
        if    (readers == 0)
            V(write_write);
    V(readers_mutex);
}

Writer:
while (true) {
    P(writers_mutex);
        writers++;
        if(writers == 1)
            P(read_write);
    V(writers_mutex);
    P(write_write);
        write();
    V(write_write);
    P(writes_mutex);
        writers--;
        if(writers == 0)
            V(read_write);
    V(writers_mutex);
}
```

## 5

### 题目

寿司店问题。假设一个寿司店有 5 个座位，如果你到达的时候有一个空座位，你可以立刻就坐。但是如果你到达的时候 5 个座位都是满的有人已经就坐，这就意味着这些人都是一起来吃饭的，那么你需要等待所有的人一起离开才能就坐。编写同步原语，实现这个场景的约束。

### 答案

**答案：**

```C
Semaphore mutex = 1;
Semaphore block = 0;    //等待队列
bool need_wait = False;     //表示寿司店5个座位已经坐满需要等待
int eating;     //记录寿司店正在吃饭的人数
int waiting;    //记录寿司店等待的人数

while(true) {
    P(mutex);
    if(need_wait) {
        waiting++;
        V(mutex);
        P(block);
    } else {
        eating++;
        if (eating = 5)
            need_wait = true;
        else    need_wait = false;
        V(mutex);
    }
    sit_and_eat();
    P(mutex);
    eating--;
    if(eating == 0) {
        int n = min(5, waiting);
        waiting -= n;
        eating += n;
        if    (eating == 5) {
            need_wait = true;
        } else {
            need_wait = false;
        }
        while(n--) {
            V(block);
        }
    }
    V(mutex);
}
```

## 6

### 题目

搜索-插入-删除问题。三个线程对一个单链表进行并发的访问，分别进行搜索、插入和删除。搜索线程仅仅读取链表，因此多个搜索线程可以并发。插入线程把数据项插入到链表最后的位置；多个插入线程必须互斥防止同时执行插入操作。但是，一个插入线程可以和多个搜索线程并发执行。最后，删除线程可以从链表中任何一个位置删除数据。一次只能有一个删除线程执行；删除线程之间，删除线程和搜索线程，删除线程和插入线程都不能同时执行。

请编写三类线程的同步互斥代码，描述这种三路的分类互斥问题。

### 答案

**答案：**

### 请编写三类线程的同步互斥代码，描述这种三路的分类互斥问题

答：

```C
Semaphore search_search = 1;    //保证搜索线程之间的互斥访问
Semaphore search_remove = 1;    //保证搜索与删除线程之间互斥
Semaphore insert_insert = 1;    //保证插入线程之间互斥
Semaphore insert_reomve = 1;    //保证插入与删除线程互斥
int searchers = 0    //记录执行的搜索线程数量
int inserters = 0;    //记录插入线程数量

searcher:
while (true) {
    P(serch_search);
        searchers++;
        if(serchers == 1)
            P(search_remove);
    V(search_search);
    search();
    P(serch_serch);
        searchers--;
        if(searchers == 0)
            V(search_remove);
    V(search_search);
}

Inserters:
while(true) {
    P(insert_insert);
        insert_insert++;
        if(inserters == 1)
            P(insert_remove);
    V(insert_insert);
    P(insert_insert);
        insert();
    V(insert_insert);
    P(insert_insert);
        if(inserters == 0)
            V(insert_remove);
    V(insert_insert);
}

remover:
while(true) {
    P(search_remove);
    P(insert_remove);
        delete();
    V(insert_remove);
    V(search_remove);
}

```
