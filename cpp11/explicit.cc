#include <iostream>

using namespace std;

class cls
{
public:
    cls(int i)
    {
        cout << i << endl;
    }
};

cls func()
{
    return 230;
}
int main()
{
    int i;
    cls c(1);
    c = func();
}
