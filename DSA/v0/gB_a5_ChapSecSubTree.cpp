/*
QUESTION:
	A book consists of chapters, chapters consist of sections and sections consist of subsections. 
	Construct a tree and print the nodes. Find the time and space requirements of your method.

OUTPUT:
	---------------
	 Book tree creation 
	---------------
	1.Create
	2.Display
	3.Quit
	Enter your choice :1
	Enter name of book :book1
	Enter number of chapters in book :2
	Enter the name of chapter 1 : chap1
	Enter number of sections in chapter chap1 : 1
	Enter name of section 1 : sec1.1
	Enter the name of chapter 2 : chap2
	Enter number of sections in chapter hap2 : 2
	Enter name of section 1 : sec2.1
	Enter name of section 2 : sec2.2
	
	----------Book Hierarchy-----------
	 Book title : book1
	Chapter 1 : chap1
	Section : 
	sec1.1
	Chapter 2 : hap2
	Section : 
	sec2.1
	ec2.2
*/

#include<iostream>
#include<string>
using namespace std;

struct node
{
	string label;
	int ch_count;
	struct node *child[10];
} * root;

class GT
{
public:
	void create_tree();
	void display(node *r1);
	
	GT()
	{
		root = NULL;
	}
};

void GT::create_tree()
{
    int tbooks, tchapters, i, j, k;
    root = new node;
    cout << "Enter name of book :";
    cin.get();
    getline(cin, root->label);  // Fixed: 'label' instead of 'el'
    
    cout << "Enter number of chapters in book :";
    cin >> tchapters;
    root->ch_count = tchapters;
    
    for (i = 0; i < tchapters; i++)
    {
        root->child[i] = new node;
        cout << "Enter the name of chapter " << i + 1 << " : ";
        cin.get();  // To clear the input buffer after reading an integer
        getline(cin, root->child[i]->label);  // Fixed: 'label' instead of 'el'
        
        cout << "Enter number of sections in chapter " << root->child[i]->label << " : ";
        cin >> root->child[i]->ch_count;
        
        for (j = 0; j < root->child[i]->ch_count; j++)
        {
            root->child[i]->child[j] = new node;
            cout << "Enter name of section " << j + 1 << " : ";
            cin.get();  // To clear the input buffer after reading an integer
            getline(cin, root->child[i]->child[j]->label);  // Fixed: 'label' instead of 'el'
        }
    }
}


void GT::display(node*r1)
{
	int i, j, k, tchapters;
	if (r1!= NULL)
	{
		cout << "\n----------Book Hierarchy-----------";
		cout << "\n Book title : " << r1->label;
		tchapters = r1->ch_count;
		for (i = 0; i < tchapters; i++)
		{
			cout << "\nChapter " << i + 1;
			cout << " : " << r1->child[i]->label;
			cout << "\nSection : ";
			for (j = 0; j < r1->child[i]->ch_count; j++)
			{
				cout << "\n"<< r1->child[i]->child[j]->label;
			}
		}
	}
	cout << endl;
}

int main()
{
	int choice;
	GT gt;
	while (1)
	{
		cout << "---------------" << endl;
		cout << " Book tree creation " << endl;
		cout << "---------------" << endl;
		cout << "1.Create" << endl;
		cout << "2.Display" << endl;
		cout << "3.Quit" << endl;
		cout << "Enter your choice :";
		cin >> choice;
		switch (choice)
		{
		case 1:
			gt.create_tree();
		case 2:
			gt.display(root);
			break;
		case 3:
			cout << "Thanks for using this proram ";
			exit(1);
		default:
			cout << "Wrong choice!!" <<endl;	
		}
	}
	return 0;
}
