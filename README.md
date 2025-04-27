# manual-book-kag

## step1.文件预处理
### pdf reader
运行以下文件，会把原始的pdf按文件输出为对应的json文件
```angular2html
src/pdf_reader.py
```
将json文件整理成txt文件存放于builder/txtfile

## step2.抽取零件类型
根据step1输出的解析后文本，使用llm根据文本提取出零件类型，并且将文件类型归类到6个大类中  
对应代码为src/classify.ipynb文件  
输出的分类好的文件存放于builder/classfied.xlsx

## step3.为建库分类数据
根据step2的输出文件，对failure type (1)和failure type (2)进行分类
### 具体分类如下：
1. failure type (1)  --> 1-3类 --> 3类里面任选6个solution  

* Spindle & Drive
* Mechanical Components
* Automation & Robotics


2. failure type (2)  --> 4-6类 --> 3类里面任选5个solution
* Coolant & Lubrication
* Electrical & Control
* Hydraulic & Pneumatic
存放至builder/classified_type.xlsx中

再从两个类中各自抽取对应数量的solution，然后存放至builder/solution_mapping

## step4.构建kag db
进入vector_db中，
以FinalOne(对应failure type (1))，
### Step 4.1：进入示例目录

```bash
cd kag/examples/baike
```

### Step 4.2：配置模型

将llm改为本地启动的Ollama接口
Example：  
```
openie_llm: &openie_llm
  base_url: http://127.0.0.1:11434/v1
  model: <你本地启动的模型型号>
  type: maas
  ```
Note:  
1.openie_llm、chat_llm都需要更改才会变成本地的模型  
2.vectorize_model向量模型如果需要使用openai的直接填入key即可,如果需要替换向量模型则需要变更```vector_dimensions```为对应的向量维度

### Step 4.3：初始化项目

先对项目进行初始化。

```bash
knext project restore --host_addr http://127.0.0.1:8887 --proj_path .
```
### Step 4.4：提交 schema

执行以下命令提交 schema

```bash
knext schema commit
```

### Step 4.5：构建知识图谱

在 [builder](./builder) 目录执行 [indexer.py](./builder/indexer.py) 构建知识图谱。

```bash
cd builder && python indexer.py && cd ..
```

FinalTwo db操作同上

## step5.跑问答
1. 完成以上步骤后，运行```vector_db/FinalOne/solver/sample_eval.py ```
2. 得到抽样后的问答结果，抽样数量可以在```sample_data = get_sample_data(2)```入参数字中调整  
3. 跑完的结果会存放于```vector_db/FinalOne/output```文件夹中
4. FinalTwo操作同上