#include<assert.h>

#define N 3
#define UNDECIDED -1

unsigned char nondet_uchar();
int nondet_int();


int a,T,E;

struct Message{
    int x;
    char valid;
    char safe;
};

struct Process{
    int id;                 //process id

    int x;

    struct Message rcv[N];  //rcv[i] indicates a message from process i in a single round
    int decide;             //value decided in a phase
};

struct Process process[N];
int sortedX[N];
int cntX[N];

void send_message(int from_id,int to_id){
    process[to_id].rcv[from_id].valid=nondet_uchar();
    __CPROVER_assume(process[to_id].rcv[from_id].valid==0 || process[to_id].rcv[from_id].valid==1);

    process[to_id].rcv[from_id].safe=nondet_uchar();
    __CPROVER_assume(process[to_id].rcv[from_id].safe==0 || process[to_id].rcv[from_id].safe==1);

    if(process[to_id].rcv[from_id].safe==1)
        process[to_id].rcv[from_id].x=process[from_id].x;
    else{
        process[to_id].rcv[from_id].x=nondet_int();
        __CPROVER_assume(process[to_id].rcv[from_id].x>=-1);
    }
}

void clear_message(int id){
    for(int i=0;i<N;i++){
        process[id].rcv[i].valid=0;
    }
}

int size_of_rcv(int id){
    int cnt=0;
    for(int i=0;i<N;i++){
        if(process[id].rcv[i].valid==1)
            cnt++;
    }
    return cnt;
}

int size_of_safe(int id){
    int cnt=0;
    for(int i=0;i<N;i++){
        if(process[id].rcv[i].valid==1 && process[id].rcv[i].safe==1)
            cnt++;
    }
    return cnt;
}

int size_of_a(int id){
    return size_of_rcv(id)-size_of_safe(id);
}

void init_process(int id,int value){
    process[id].id=id;
    process[id].x=nondet_int();
    process[id].decide=UNDECIDED;

    __CPROVER_assume(process[id].x>=-1);
}

int send_1(int id,int phase){
    for(int i=0;i<N;i++){
        send_message(id,i);
    }
    return 0;
}

int transition_1(int id,int phase){
    int tmpX,maxcnt;

    for (int i=0;i<N;i++){
        if(process[id].rcv[i].valid==1)
            sortedX[i] = process[id].rcv[i].x;
        else
            sortedX[i] = -1;
        cntX[i]=1;
    }
    for(int i=0;i<N;i++){
        for(int j=0;j<N-1;j++){
            if(sortedX[j]==-1 || (sortedX[j+1]!=-1 && sortedX[j]>sortedX[j+1])){
                tmpX=sortedX[j];
                sortedX[j]=sortedX[j+1];
                sortedX[j+1]=tmpX;
            }
        }
    }
    tmpX=sortedX[0];
    maxcnt=1;
    for(int i=1;i<N;i++){
        if(sortedX[i]!=-1 && sortedX[i]==sortedX[i-1]){
            cntX[i]=cntX[i-1]+1;
            if(cntX[i]>maxcnt){
                maxcnt=cntX[i];
                tmpX=sortedX[i];
            }
        }
    }

    if(size_of_rcv(id)>T){
        process[id].x=tmpX;
    }
    if(maxcnt>E){
        process[id].decide=tmpX;
    }
    clear_message(id);
    return 0;
}

int assume_Univalence(int v){
    int tmpX;
    for(int i=0;i<N;i++){
        sortedX[i]=process[i].x;
        cntX[i]=1;
    }
    for(int i=0;i<N;i++){
        for(int j=0;j<N-1;j++){
            if(sortedX[j+1]==v){
                tmpX=sortedX[j];
                sortedX[j]=sortedX[j+1];
                sortedX[j+1]=tmpX;
            }
        }
    }
    for(int i=0;i<N;i++){
        __CPROVER_assume(sortedX[i]==v || i>E);
    }
}
int is_Univalence(int v){
    int tmpX;
    for(int i=0;i<N;i++){
        sortedX[i]=process[i].x;
        cntX[i]=1;
    }
    for(int i=0;i<N;i++){
        for(int j=0;j<N-1;j++){
            if(sortedX[j+1]==v){
                tmpX=sortedX[j];
                sortedX[j]=sortedX[j+1];
                sortedX[j+1]=tmpX;
            }
        }
    }
    for(int i=0;i<N;i++){
        if(!(sortedX[i]==v || i>E))
            return 0;
    }
    return 1;
}

int is_Singular(int v){
    for(int i=0;i<N;i++){
        if(process[i].decide!=UNDECIDED && process[i].decide!=v)
            return 0;
    }
    return 1;
}
int is_Decide(int v){
    for(int i=0;i<N;i++){
        if(process[i].decide==v)
            return 1;
    }
    return 0;
}

int main(){
    a=nondet_int();
    T=nondet_int();
    E=nondet_int();
    __CPROVER_assume(a>=0 && a<=N);
    __CPROVER_assume(E>=0 && E<N);
    __CPROVER_assume(T>=2*(N+2*a-E) && T<N);

    int value=nondet_int();
    __CPROVER_assume(value>=0);
    
    for(int i=0;i<N;i++){
        init_process(i,(i+1)*10);
    }
    
    //assume_Univalence(value);

    int phase=1;
    for(int i=0;i<N;i++)
        send_1(i,phase);
    for(int i=0;i<N;i++)
        __CPROVER_assume(size_of_a(i)<=a);
    for(int i=0;i<N;i++)
        transition_1(i,phase);
    phase++;

    __CPROVER_assume(is_Decide(value));
    assert(is_Singular(value) && !is_Univalence(value));
    
    return 0;
}
