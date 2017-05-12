#include<stdio.h>  
#include<stdlib.h>  
#include<math.h>  
#include<time.h> 

#include "dbscan.h"

//#define INITIALASSIGN_COREOBJECT      100  
//#define INCREASEMENT_COREOBJECT       100       


int Dbsacn::calcu(string str, int count)
{
	//if (argc != 5)
	//{
	//	printf("this program need 5 parematers to run,"
	//		"\n\t\tthe first to indicate the neighborhood"
	//		"\n\t\tthe second to indicate the MinPts"
	//		"\n\t\tthe third to indicate the filename contain data"
	//		"\n\t\tthe fourth to indicate the data size");
	//	exit(0);
	//}
	//srand((unsigned)time(NULL));
	//neighborhood = atof(argv[1]);
	//MinPts = atoi(argv[2]);
	//strcat(filename, argv[3]);
	//data_size = atoi(argv[4]);

	srand((unsigned)time(NULL));
	neighborhood = 50;// atof(argv[1]);
	minPts = 10;// atoi(argv[2]);
	str_fileName = str;
	data_size = count;// atoi(argv[4]);

	Init();
	ReadData();
	calculateDistance_BetweenAll();
	statisticCoreObject();
	//showInformation();  
	setCoreObject();
	//testQueue();  
	DBSCAN();
	system("pause");
	return 0;
}

/*
* initialization
* */
int Dbsacn::Init()
{
	point = (Point*)malloc(sizeof(struct Point) * (data_size + 1));
	if (!point)
	{
		printf("point malloc error");
		return 1;
	}

	coreObject_Collection = (CoreObject*)malloc(sizeof(struct CoreObject) * (data_size + 1));
	if (!coreObject_Collection)
	{
		printf("coreObject_Collection malloc error!");
		return 2;
	}
	int coreObject;         //traverse  
	for (coreObject = 1; coreObject <= data_size; coreObject++)
	{
		coreObject_Collection[coreObject].coreObjectID = 0;             //if the value equal 0 denote it's not core object  
		coreObject_Collection[coreObject].reachableSize = 0;                //INITIALASSIGN_DIRECTLYDENSITYREACHABLE  
		coreObject_Collection[coreObject].capacity = INITIALASSIGN_DIRECTLYDENSITYREACHABLE;
		coreObject_Collection[coreObject].directlyDensityReachable = (int*)malloc(sizeof(int)* (INITIALASSIGN_DIRECTLYDENSITYREACHABLE + 1));
		if (!coreObject_Collection[coreObject].directlyDensityReachable)
		{
			printf("coreObject_Collection malloc error: %d", coreObject);
			return 3;
		}
	}
}

/*
* read data from file;
*  set the value of point
* */
int Dbsacn::ReadData()
{
	FILE* fread;
	if (NULL == (fread = fopen(str_fileName.c_str(), "r")))
	{
		printf("open file(%s) error!", str_fileName.c_str());
		return -1;
	}
	for (int i = 1; i <= data_size; i++)
	{
		double x, y;
		if (2 != fscanf(fread, "%lf\t%lf", &x, &y))// &point[i].x, &point[i].y))
		{
			printf("scanf error: %d", i);
			return i;
		}
		point[i].x = x;
		point[i].y = y;
	}
	return 0;
}

/*
* calculate distance between two point
* */
double Dbsacn::calculateDistance_BetweenTwo(int firstPoint, int secondPoint)
{
	double temp = sqrt(pow((double)(point[firstPoint].x - point[secondPoint].x), 2) + pow((double)(point[firstPoint].y - point[secondPoint].y), 2));
	return temp;
}

/*
* calculate distance bewteen specifed point to all others points
* and seek the directly_density_reachable of the specified point &pointID
* */
int Dbsacn::calculateDistance_BetweenOneToAll(int pointID)
{
	int i;
	for (i = 1; i <= data_size; i++)
	{
		if (i != pointID)
		{
			if (calculateDistance_BetweenTwo(pointID, i) <= neighborhood)
			{
				coreObject_Collection[pointID].reachableSize++;
				if (coreObject_Collection[pointID].reachableSize > coreObject_Collection[pointID].capacity)
				{
					printf("\nrealloc\n\n");
					coreObject_Collection[pointID].directlyDensityReachable = (int*)realloc(coreObject_Collection[pointID].directlyDensityReachable, sizeof(int)* (coreObject_Collection[pointID].capacity + INCREASEMENT_DIRECTLYDENSITYREACHABLE));
					if (!coreObject_Collection[pointID].directlyDensityReachable)
					{
						printf("coreObject_Collection[%d].directlyDensityReachable realloc error", i);
						return 1;
					}
					coreObject_Collection[pointID].capacity += INCREASEMENT_DIRECTLYDENSITYREACHABLE;
				}
				coreObject_Collection[pointID].directlyDensityReachable[coreObject_Collection[pointID].reachableSize] = i;
			}
		}
	}
	return 0;
}

/*
* calculate distance between all points
* */
void Dbsacn::calculateDistance_BetweenAll()
{
	int i;          //traverse all the data_size  
	for (i = 1; i <= data_size; i++)
	{
		calculateDistance_BetweenOneToAll(i);
	}
}

/*
* specify the core object by statisticing the number of directly_density_reachable for all points
* the value of coreObject in the struct of coreObject_Collection be used to denote whether or not a core object
* */
void Dbsacn::statisticCoreObject()
{
	int i;
	for (i = 1; i <= data_size; i++)
	{
		if (coreObject_Collection[i].reachableSize >= minPts - 1)           //core object  
		{
			size_of_core_object++;
			coreObject_Collection[i].coreObjectID = i;          //ueing non_zero value to denote this point is a core_object  
		}
	}
}

/*
* show the struct of the directly_density_reachable of all coreObject
* */
void Dbsacn::showInformation()
{
	int direct_reachable;
	int coreObject;
	for (coreObject = 1; coreObject <= data_size; coreObject++)
	{
		printf("%d---", coreObject_Collection[coreObject].coreObjectID);
		for (direct_reachable = 1; direct_reachable <= coreObject_Collection[coreObject].reachableSize; direct_reachable++)
		{
			printf("%d ", coreObject_Collection[coreObject].directlyDensityReachable[direct_reachable]);
		}
		printf("\n");
	}
}

/*
* set the struct of @coreObject in term of the result of coreObject_Collection
* */
int Dbsacn::setCoreObject()
{
	coreObject = (CoreObject*)malloc(sizeof(struct CoreObject) * (size_of_core_object + 1));
	if (!coreObject)
	{
		printf("coreObject malloc error!");
		return 1;
	}
	int i;
	int j;
	int count = 1;
	for (i = 1; i <= data_size; i++)
	{
		if (coreObject_Collection[i].reachableSize >= minPts - 1)
		{
			coreObject[count].coreObjectID = i;
			coreObject[count].directlyDensityReachable = (int*)malloc(sizeof(int)* (coreObject_Collection[i].reachableSize + 1));
			if (!coreObject[count].directlyDensityReachable)
			{
				printf("coreObject[%d].directlyDensityReachable malloc error!");
				return 2;
			}
			for (j = 1; j <= coreObject_Collection[i].reachableSize; j++)
			{
				coreObject[count].directlyDensityReachable[j] = coreObject_Collection[i].directlyDensityReachable[j];
			}
			coreObject[count].capacity = 0;     //change its function to flag whether this core object has beed selected  
			coreObject[count].reachableSize = coreObject_Collection[i].reachableSize;
			count++;
		}
	}
	return 0;
}

/*
* some preparatory for the algorithem DBSCAN
*  create the set of Un-accessed data
* */
int* Dbsacn::preparatory_DBSCAN()
{
	//initial the Un-accessed data  
	int* UnaccessedData;
	UnaccessedData = (int*)malloc(sizeof(int)* (data_size + 1));
	if (!UnaccessedData)
	{
		printf("UnaccessedData malloc error!");
		return 0;
	}
	int i;
	for (i = 0; i <= data_size; i++)
		UnaccessedData[i] = 0;          //0 denote haven't been visited  
	//seek the noise  
	for (i = 1; i <= data_size; i++)
	{
		if (0 == coreObject_Collection[i].reachableSize)
		{
			UnaccessedData[i] = -1;     //uses non-zero to denote the noise  
		}
	}

	return UnaccessedData;
}

/********************************************************************************************************************
********************************************************************************************************************
*
*                          DBSCAN
*
********************************************************************************************************************
********************************************************************************************************************/
int Dbsacn::DBSCAN()
{
	int* un_accessed_data = preparatory_DBSCAN();
	int* old_unAccessedData;                                //save the original information of un_accessed_data  
	int i;
	old_unAccessedData = (int*)malloc(sizeof(int)* (data_size + 1));
	if (!old_unAccessedData)
	{
		printf("old_unAccessedData malloc error!");
		return 1;
	}
	for (i = 1; i <= data_size; i++)
		old_unAccessedData[i] = un_accessed_data[i];

	//initial the queue for containing the directly_density_reachable  
	LinkQueue workQueue;
	initialQueue(&workQueue);

	int cluster_count = 0;
	int randomCoreObjectID;
	int pop_Queue_ID = 0;
	int test_counter_1 = 1;
	int test_counter_2 = 1;

	while (existCoreObject() != 0)                             //still exist core object in the @coreObject  
	{
		printf("\n---------%d\n", test_counter_1);
		refreshOld_unAccessed_Set(un_accessed_data, old_unAccessedData);
		randomCoreObjectID = getRandomCoreObject();
		addToQueue_baseCoreObject(&workQueue, randomCoreObjectID);
		updateUnaccessSet(un_accessed_data, randomCoreObjectID);
		test_counter_2 = 1;
		while (!isEmptyQueue(workQueue))
		{
			printf("\n\t++++++++++++%d\n", test_counter_2++);
			deleteQueue(&workQueue, &pop_Queue_ID);
			if (coreObject_Collection[pop_Queue_ID].reachableSize >= minPts - 1)
			{
				addToQueue_intersectionBased(&workQueue, un_accessed_data, pop_Queue_ID);
			}
		}
		cluster_count += 1;
		printf("\ncluster_count is %d\n", cluster_count);
		getCluster(un_accessed_data, old_unAccessedData, cluster_count);
		updateCoreObject(un_accessed_data);
		test_counter_1++;
	}
	saveNoise(un_accessed_data);
	return 0;
}


/*
* the purpose of this function is to judeg whether or not exist core_object in the @coreObject
*  the component in the struct of coreObject is to determin the existence of the corresponding core object
*      return 0: non-exist
*      return 1: exist
* */
int Dbsacn::existCoreObject()
{
	int core;
	for (core = 1; core <= size_of_core_object; core++)
	{
		if (0 == coreObject[core].capacity)
		{
			return 1;
		}
	}
	return 0;
}
/*
*
* */
void Dbsacn::refreshOld_unAccessed_Set(int* un_accessed_data, int* old_unAccessedData)
{
	int i;
	for (i = 1; i <= data_size; i++)
	{
		old_unAccessedData[i] = un_accessed_data[i];
	}
}
/*
* select a core_object randomly
*  the retuen value is the ID of selected core_object
* */
int Dbsacn::getRandomCoreObject()
{
	//select a core object randomly, and insert the directly_density_reachable of it into to queue.  
	int i, j;
	int core_object_count = 0;
	for (i = 1; i <= size_of_core_object; i++)
	{
		if (coreObject[i].capacity == 0)
			core_object_count += 1;
	}
	int* auxiliaryArray;
	auxiliaryArray = (int*)malloc(sizeof(int)* (core_object_count + 1));
	if (!auxiliaryArray)
	{
		printf("auxiliaryArray malloc error!\n");
		return 0;
	}

	int counter_au = 1;
	for (i = 1; i <= size_of_core_object; i++)
	{
		if (coreObject[i].capacity == 0)       //still have not been selected  
		{
			auxiliaryArray[counter_au++] = coreObject[i].coreObjectID;
		}
	}
	int randomCoreObjectID;
	int randomIndex;
	int length = core_object_count;
	randomIndex = rand() % length + 1;
	randomCoreObjectID = auxiliaryArray[randomIndex];
	auxiliaryArray[randomIndex] = auxiliaryArray[length--];
	return randomCoreObjectID;
}
/*
* after selected a random core_object, we need to add the directly_density_reachable of this core object to the queue
*  particular note: instead use the coreObject, we need to use the original struct coreObject_Collection,
*           because of the incomplete in the index of @coreObject.
*
* */
void Dbsacn::addToQueue_baseCoreObject(LinkQueue* LQ, int coreObjectID)
{
	int i;
	//printf("add to queue, the reachable of coreObject is %d\n", coreObject_Collection[coreObjectID].reachableSize);  
	for (i = 1; i <= coreObject_Collection[coreObjectID].reachableSize; i++)
	{
		insertQueue(LQ, coreObject_Collection[coreObjectID].directlyDensityReachable[i]);
	}
}
/*
* after selected a random core_object. we need to update the information about un-accessed-set
*  particular note: instead use the coreObject, we need to use the original struct coreObject_Collection,
*           because of the incomplete in the index of @coreObject.
* */
void Dbsacn::updateUnaccessSet(int* un_accessed_data, int randomCoreObjectID)
{
	int i;
	for (i = 1; i <= coreObject_Collection[randomCoreObjectID].reachableSize; i++)
	{
		un_accessed_data[coreObject_Collection[randomCoreObjectID].directlyDensityReachable[i]] = coreObject_Collection[randomCoreObjectID].directlyDensityReachable[i];
	}
	un_accessed_data[randomCoreObjectID] = randomCoreObjectID;      //core object has visited  
}
/*
* if exist the core_object in the list of directly_density_reachable of other core_object
* add the element in the @workqueue which is not even dealed with of the core_object
* and update the @un_accessed_set.
* */
void Dbsacn::addToQueue_intersectionBased(LinkQueue* LQ, int* un_accessed_set, int pop_Queue_ID)
{
	int core_DDR;           //trverse the core_directly_reachable of pop_Queue_ID  
	for (core_DDR = 1; core_DDR <= coreObject_Collection[pop_Queue_ID].reachableSize; core_DDR++)
	{
		if (0 == un_accessed_set[coreObject_Collection[pop_Queue_ID].directlyDensityReachable[core_DDR]])
		{
			insertQueue(LQ, coreObject_Collection[pop_Queue_ID].directlyDensityReachable[core_DDR]);
			un_accessed_set[coreObject_Collection[pop_Queue_ID].directlyDensityReachable[core_DDR]] = coreObject_Collection[pop_Queue_ID].directlyDensityReachable[core_DDR];
		}
	}
}
/*
* get cluster based on a core object
* */
int Dbsacn::getCluster(int* un_accessed_data, int* old_unAccessedData, int clusterID)
{
	char filename[200];
	//sprintf(filename, ".//DBSCAN_cluster//cluster_%d.data", clusterID);
	sprintf(filename, "cluster_%d.data", clusterID);
	FILE* fwrite;
	if (NULL == (fwrite = fopen(filename, "w")))
	{
		printf("open file(%s) error", filename);
		return 1;
	}
	int i;
	for (i = 1; i <= data_size; i++)
	{
		if (un_accessed_data[i] != old_unAccessedData[i])
		{
			fprintf(fwrite, "%f\t%f\n", point[i].x, point[i].y);
		}
	}
	fclose(fwrite);
	return 0;
}
/*
*
* */
void Dbsacn::updateCoreObject(int* un_accessed_data)
{
	int i;
	for (i = 1; i <= size_of_core_object; i++)
	{
		if (0 != un_accessed_data[coreObject[i].coreObjectID])
		{
			coreObject[i].capacity = 1;         //denote this core object has been dealed  
		}
	}
}
int Dbsacn::saveNoise(int* un_accessed_data)
{
	FILE* fwriteNoise;
	if (NULL == (fwriteNoise = fopen("noise.data", "w")))
	{
		printf("open file(nosie.data) error!");
		return 1;
	}
	int i;
	printf("\nshow the noise data:\n");
	for (i = 1; i <= data_size; i++)
	{
		if (un_accessed_data[i] == -1 || un_accessed_data[i] == 0)
		{
			fprintf(fwriteNoise, "%f\t%f\n", point[i].x, point[i].y);
			printf("%f\t%f\n", point[i].x, point[i].y);
		}
	}
	return 2;
}

/*
* some operation about queue
* */
bool Dbsacn::initialQueue(LinkQueue* LQ)
{
	LQ->front = (QueueNodePtr)malloc(sizeof(QueueNode));
	if (!LQ->front)
	{
		printf("Queue initial malloc error!");
		return false;
	}
	LQ->rear = LQ->front;
	LQ->rear->next = NULL;
	return true;
}
bool Dbsacn::insertQueue(LinkQueue* LQ, int pointID)
{
	QueueNode* newNode;
	newNode = (QueueNodePtr)malloc(sizeof(QueueNode));
	if (!newNode)
	{
		printf("insert queue malloc error %d\n", pointID);
		return false;
	}
	newNode->data = pointID;
	newNode->next = LQ->rear;
	LQ->rear->next = newNode;
	LQ->rear = newNode;
	return true;
}
bool Dbsacn::deleteQueue(LinkQueue* LQ, int* pointID)
{
	QueueNode* p = LQ->front->next;
	*pointID = p->data;
	LQ->front->next = p->next;
	if (p == LQ->rear)
		LQ->rear = LQ->front;
	free(p);
	return true;
}
bool Dbsacn::printQueue(LinkQueue LQ)
{
	if (1 == isEmptyQueue(LQ))
	{
		printf("\nqueue is empty\n");
		return false;
	}
	LQ.front = LQ.front->next;
	while (LQ.front != LQ.rear)
	{
		printf("%d ", LQ.front->data);
		LQ.front = LQ.front->next;
	}
	printf("%d\n", LQ.front->data);
	return true;
}
int Dbsacn::isEmptyQueue(LinkQueue LQ)
{
	return LQ.front == LQ.rear ? 1 : 0;
}
//test  
void Dbsacn::testQueue()
{
	LinkQueue L;
	initialQueue(&L);
	insertQueue(&L, 1);
	insertQueue(&L, 2);
	insertQueue(&L, 3);
	insertQueue(&L, 4);
	insertQueue(&L, 5);
	printQueue(L);
	int test;
	deleteQueue(&L, &test);
	deleteQueue(&L, &test);
	deleteQueue(&L, &test);
	deleteQueue(&L, &test);
	printf("is empty = %d\n", isEmptyQueue(L));
	deleteQueue(&L, &test);
	printf("is empty = %d\n", isEmptyQueue(L));
	printQueue(L);
}



//////////////////////////////////////////////////////////////////////////
/*
 Other code
*/

//#include<stdio.h>
//#include<string.h>
//#include<math.h>
//#define TOTALPOINT 100
//typedef  int  DATATYPE;   //队列元素的数据类型
//#define  maxsize  64       //队列可能达到的容量
//
//struct List
//{
//	int data[TOTALPOINT];
//	int head;
//	int tail;
//}ClusterList;
//
//struct Node
//{
//	int x;
//	int y;
//}database[TOTALPOINT];
//bool Neighbor[TOTALPOINT][TOTALPOINT];
//int ClusterNo[TOTALPOINT];
//typedef  struct
//{
//	DATATYPE data[maxsize];//队中元素
//	int front, rear;	//队头元素下标、队尾元素后面位置的下标
//} SEQQUEUE;
////1．顺序循环队列置队空：
//void QueueInit(SEQQUEUE *sq)
////将顺序循环队列sq置空（初始化）
//{
//	sq->front = 0;
//	sq->rear = 0;
//}
////2.  判断顺序循环队列是否为空
//int QueueIsEmpty(SEQQUEUE sq)
////如果顺序循环队列sq为空，成功返回1，否则返回0
//{
//	if (sq.rear == sq.front)
//		return(1);
//	else
//		return(0);
//}
////3.  顺序循环队列取队头元素
//int QueueFront(SEQQUEUE sq, DATATYPE *e)
////将顺序循环队列sq的队头元素保存到e所指地址，成功返回1，失败返回0
//{
//	if (QueueIsEmpty(sq))
//	{
//		printf("queue is empty!\n");
//		return 0;
//	}
//	else
//	{
//		*e = sq.data[(sq.front)];
//		return 1;
//	}
//}
////4．顺序循环队列入队
//int QueueIn(SEQQUEUE *sq, DATATYPE x)
////将元素x入队列sq的队尾，成功返回1，失败返回0
//{
//	if (sq->front == (sq->rear + 1) % maxsize)
//	{
//		printf("queue is full!\n"); return 0;
//	}
//	else
//	{
//		sq->data[sq->rear] = x;
//		sq->rear = (sq->rear + 1) % maxsize;
//		return(1);
//	}
//}
////5.  顺序循环队列出队
//int QueueOut(SEQQUEUE *sq)
////将队列sq队首元素出队列，成功返回1,失败返回0
//{
//	if (QueueIsEmpty(*sq))
//	{
//		printf("queue is empty!\n"); return 0;
//	}
//	else
//	{
//		sq->front = (sq->front + 1) % maxsize;
//		return  1;
//	}
//}
//
//float dist(float *a, float *b, int n) //a、b为两个向量 n是维度，返回欧式距离
//{
//	float re = 0;
//	for (int i = 0; i<n; i++)
//	{
//		re += ((a[i] - b[i])*(a[i] - b[i]));
//	}
//	re = sqrt(re);
//	return re;
//}
///*float dist(Node a,Node b) //a、b为两个向量 n是维度，返回欧式距离
//{
//float re=0;
//for(int i=0;i<2;i++)
//{
//re+=((a-b[i])*(a[i]-b[i]))[i];
//}
//re=sqrt(re);
//return re;
//}*/
//double dist(Node a, Node b)
//{
//	double dis;
//	dis = (a.x - b.x)*(a.x - b.x) + (a.y - b.y)*(a.y - b.y);
//	dis = sqrt(dis);
//	return dis;
//}
//void main()
//{
//	int x, n, i, j, NeighborPointsNum, CurrentClusterNO;
//	SEQQUEUE list;
//	printf("请输入点的个数为:");
//	scanf("%d", &n);
//	for (i = 0; i<n; i++)
//	{
//		printf("请输入第%d个数的点为:", i);
//		scanf("%d%d", &database[i].x, &database[i].y);
//		ClusterNo[i] = -1;
//	}
//	QueueInit(&list);
//	CurrentClusterNO = 0;
//	//计算临近
//	for (i = 0; i<n; i++)
//	{
//		for (j = 0; j<n; j++)
//		{
//			if (dist(database[i], database[j]) <= 1)//if (dist(database[i],database[j])<= )
//			{
//				Neighbor[i][j] = true;
//				Neighbor[j][i] = true;
//			}
//		}
//	}
//	//聚类划分
//
//	for (i = 0; i<n; i++)
//	{
//		if (ClusterNo[i] >= 0) continue;
//		NeighborPointsNum = 0;
//		for (j = 0; j<n; j++)
//		if (Neighbor[i][j] == true)
//			NeighborPointsNum++;
//		if (NeighborPointsNum >= 4)    //if( NeighborPointsNum >= MinPts)此处令MinPst=4
//		{
//			CurrentClusterNO++;
//			QueueIn(&list, i);
//			ClusterNo[i] = 0;
//		}
//		while (QueueIsEmpty(list) == 0)
//		{
//			QueueFront(list, &x);
//			QueueOut(&list);
//			if (ClusterNo[x] <= 0)
//			{
//				ClusterNo[x] = CurrentClusterNO;
//				NeighborPointsNum = 0;
//				for (j = 0; j<n; j++)
//				if (Neighbor[x][j] == true)NeighborPointsNum++;
//				if (NeighborPointsNum >= 4)
//				{
//					for (j = 0; j<n; j++)
//					if ((Neighbor[x][j] == true) && (ClusterNo[j]<0))
//					{
//						QueueIn(&list, j); ClusterNo[j] = 0;
//					}
//				}
//			}
//
//
//		}
//	}
//	//聚类结果输出
//	for (i = -1; i <= CurrentClusterNO; i++)
//	{
//		if (i == -1)
//			printf("\n输出噪声数据:");
//		else
//			printf("\n输出第%d簇的对象：", i);
//		for (j = 0; j<n; j++)
//		if (ClusterNo[j] == i) printf("%d\t\n", j);
//	}
//	getchar();
//}
