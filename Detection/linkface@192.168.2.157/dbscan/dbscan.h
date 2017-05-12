//////////////////////////////////////////////////////////////////////////


#ifndef DBSCAN_H
#define DBSCAN_H

#include<string>

using namespace std;


#define INITIALASSIGN_DIRECTLYDENSITYREACHABLE  100 
#define INCREASEMENT_DIRECTLYDENSITYREACHABLE   10 

int size_of_core_object;

typedef struct Point
{
	double x;
	double y;
}Point;
Point* point;

typedef struct CoreObject
{
	int coreObjectID;
	int* directlyDensityReachable;  //store the directly density_reachable point of corePointID  
	int reachableSize;      //the number of directly density reachable  
	int capacity;           //the current capacity of the dynamic array @directlyDensityReachable  
}CoreObject;
CoreObject* coreObject_Collection;  //collectint the core_object  
CoreObject* coreObject;         //collected core_object  

//sequence queue  
typedef struct QueueNode
{
	int data;
	struct QueueNode* next;
}QueueNode, *QueueNodePtr;
typedef struct LinkQueue
{
	QueueNodePtr front;
	QueueNodePtr rear;
}LinkQueue;

class Dbsacn
{
public:
	Dbsacn();
	~Dbsacn();

public:
	int calcu(string str, int count);

private:
	bool initialQueue(LinkQueue*);
	bool insertQueue(LinkQueue*, int);
	bool deleteQueue(LinkQueue*, int*);
	bool printQueue(LinkQueue);
	void testQueue();
	int isEmptyQueue(LinkQueue);

	//sequence queue END  

	int Init();
	int ReadData();
	double calculateDistance_BetweenTwo(int, int);
	int calculateDistance_BetweenOneToAll(int);
	void calculateDistance_BetweenAll();
	void statisticCoreObject();
	void showInformation();
	int setCoreObject();
	int* preparatory_DBSCAN();
	int DBSCAN();
	void refreshOld_unAccessed_Set(int*, int*);
	int existCoreObject();
	int getRandomCoreObject();
	void addToQueue_baseCoreObject(LinkQueue*, int);
	void updateUnaccessSet(int*, int);
	void addToQueue_intersectionBased(LinkQueue*, int*, int);
	int getCluster(int*, int*, int);
	void updateCoreObject(int*);
	int saveNoise(int*);

private:
	double neighborhood;
	int minPts;
	string str_fileName;
	int data_size;

};

#endif //DBSCAN_H