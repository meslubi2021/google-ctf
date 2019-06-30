#include <stdio.h> //for printf
#include <stdbool.h> //for bool


#define N 9009131337
#define CS 100000000	/* cache size */

typedef unsigned long ulong;
typedef unsigned long long ull;

struct hailstoneEntry
{
    ull key;
    ulong steps;
};


struct hailstoneEntry hailstoneCache[CS] = {0};


void addToCache(ull key, ulong steps)
{
    ulong pos = key % CS;
    hailstoneCache[pos].key = key;
    hailstoneCache[pos].steps = steps;
}

ulong getFromCache(ull key)
{
    ulong pos = key % CS;
    if( hailstoneCache[pos].key != key )
    {
        return 0;
    }
    return hailstoneCache[pos].steps;
}



ull hailstoneSum(ull n)
{
    ull totalSteps = 0;
    ull percent = N / 100;
	for (ull start_num = 1; start_num <= N; ++start_num) 
    {
        ull num = start_num;
		ulong steps = 0;
        ulong deltaSteps = 0;
        ulong missedNum = 0;
		while( num != 1 )
        {
			if( num & 0x1 ) //odd
            {
				num += (num >> 1) + 1; //num = (3 * num + 1) / 2
				steps += 2;
            }
			if( (num & 0x1) == 0 ) //even
            {
                num >>= 1;
				steps += 1;
            }
            
            //check cache
            if( num < start_num )
            {
                //could be in cache
                ulong cacheSteps = getFromCache(num);
                if( cacheSteps > 0 )
                {
                    steps += cacheSteps;
                    num = 1;
                }
                else
                {
                    //cache miss
                    if(missedNum == 0) 
                    {
                        missedNum = num;
                        deltaSteps = steps;
                    }
                }
            }
        }
        
        //write to cache the first cache miss
        if(missedNum != 0 )
        {
            addToCache(missedNum, steps - deltaSteps);
        }
        totalSteps += steps;

        if(start_num % percent == 0)
        {
            printf("%llu%% subtotal = %llu\n", (start_num / percent), totalSteps);
        }
	}
    return totalSteps;
}
 
int main()
{
    ull total = hailstoneSum(N);

    ull fib_value = fib(N, total);

	printf("result = %llx\n", total);
	return 0;
}