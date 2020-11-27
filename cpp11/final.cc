#include <iostream>

using namespace std;

class parent
{
public:
    int x;
    virtual void func() final
    {
        cout << "parent" << endl;
    }
};

class child : public parent
{
public:
    int x;
    void func()
    {
        cout << "child" << endl;
    }
};

int main()
{
    child c;
    c.func();
    return 0;
}