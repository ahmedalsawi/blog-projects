#include <iostream>
using namespace std;
class cls
{

public:
    int x;
    void func()
    {
        throw 3;
    }
    void func2() noexcept
    {
        throw 3;
    }
};
int main()
{
    cls c;
    try
    {

        // c.func();  // print 3
        c.func2(); // crashes as function
    }
    catch (int e)
    {
        cout << e << endl;
    }
}