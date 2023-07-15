// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#include "dictionary.h"

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Represents a node in a hash table
typedef struct node
{
    bool isword;
    struct node *children[N]
}
node;

// Hash table
node *trie[N];

// dictionary size counter
int dict_size = 0;

bool search_trie(node *n, const char *word)
{
    if (n == NULL)
    {
        return false;
    }
    int x = strlen(word);
    for (int i = 0; i < x; i++)
    {
        n = n->children[word[i]-'a'];
    }
    if(n->isword)
    {
        return true;
    }
    else
    {
        return false;
    }
}

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    return search_trie(trie, tolower(word));
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    // Function should take a string and return an index
    // This hash function adds the ASCII values of all characters in the word together
    int x = strlen(word);
    for(int i = 0; i < x; i++)
    {
        n->children[word[i]-'a'];
    }
    n->isword = true;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open dictionary file
    FILE *dict_pointer = fopen(dictionary, "r");

    // Check if null
    if (dictionary == NULL)
    {
        printf("Unable to open %s\n", dictionary);
        return false;
    }

    // initialize Word-Array
    char next_word[LENGTH + 1];

    // Read words into Hashtable
    while (fscanf(dict_pointer, "%s", next_word) == 1)
    {
        node *n = malloc(sizeof(node));
        if(n == NULL)
        {
            return false;
        }

        strcpy(n->word, next_word);
        n->next=NULL;
        int hash_Value = hash(next_word);
        table[hash_Value] = n;
        dict_size++;
    }
    fclose(dict_pointer);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return dict_size;
}

void free_Node(node *n)
{
    if(n == NULL)
    {
        return;
    }
    free_Node(n->next);
    free(n);
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        // Zeiger zuweisen
        node *n = table[i];

        // Rufe rekursive Funktion auf, um Nodes freizugeben
        free_Node(n);
    }
    return true;
}