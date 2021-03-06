#include "sphereTree.h"

using namespace Foundation;
using namespace Foundation::Entities;

SphereTree::SphereTree()
{
    m_nMinRadius = 10;
    m_nMaxRadius = 200;

    m_pRoot = new SphereNode(m_nMinRadius, m_nMaxRadius, false, 3);
    m_pRoot->m_bRootNode = true;
    m_pRoot->m_pParentNode = NULL;

    m_nDebugDataCount = 0;
}

SphereTree::~SphereTree()
{
    destroy();
}

void SphereTree::destroy()
{
    m_pRoot->destroy();
    delete m_pRoot;
}

vector<SphereData *>::iterator& SphereTree::addData(SphereData *_data)
{
    //f_printf("SphereTree Adding Data... (Pos: %f, %f, %f)\n", _data->getPosition()[0], _data->getPosition()[1], _data->getPosition()[2]);

    vector<SphereData *>::iterator *itr = new vector<SphereData *>::iterator();
    //SphereData *dataCopy = new SphereData(_data);

    // Insert at the end, retrieve the iterator to the data
    //m_uDataStore.insert(m_uDataStore.end(), _data);
    m_nDebugDataCount++;

    m_pRoot->addSphereData(_data);
    
    return (*itr);
}

void SphereTree::removeData(vector<SphereData *>::iterator& _iterator)
{
}

unsigned int SphereTree::getChildCount()
{
    return m_pRoot->getChildCount();
}

unsigned int SphereTree::getMaxDepth()
{
    return m_pRoot->getMaxDepth();
}

void SphereTree::setMaxBucketSize(unsigned int _size)
{
    if (_size < 2)
        _size = 2;
    else if (_size > 20)
        _size = 20;

    m_pRoot->setMaxBucketSize(_size, true);
}

void SphereTree::update()
{
    m_pRoot->update();
}

void SphereTree::dump()
{
    f_printf("========================================================================\nSphereTree Dump:\n");
    m_pRoot->dump(0);
    f_printf("========================================================================\n");
}

void SphereTree::debugRender(const char* _sSceneManagerName, int _nRenderLevel, char _nTeamBitfieldFlag)
{
    m_pRoot->debugRender(_sSceneManagerName, true, _nTeamBitfieldFlag, _nRenderLevel, 0);
}

void SphereTree::clearDebugRender(const char* _sSceneManagerName)
{
    m_pRoot->clearDebugRender(_sSceneManagerName);
}
