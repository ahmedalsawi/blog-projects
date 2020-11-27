#include <iostream>
using namespace std;
class cls
{

public:
    int x;
    void func() const
    {
        // x = 0;
        const_cast<int &>(x) = 3;
        std::cout << x << endl;
    }
};
int main()
{
    cls c;
    c.func();
}