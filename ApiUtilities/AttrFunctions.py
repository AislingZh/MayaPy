import maya.api.OpenMaya as OpenMaya
import pymel.core as pm
import logging
logging.basicConfig()
logger = logging.getLogger('AttrFunctions:')
logger.setLevel(logging.DEBUG)

def findAttr(attr, *args):
    """
    Args:
        attr: Attribute desired
        *args: objects we want to check, if no *args check entire scene

    Returns: Pymel objects List that contain the attribute
    """
    
    mselList = OpenMaya.MSelectionList()
    # if some args are given
    if len(args):
        for i in args:
            mselList.add(i)
    # no args check entire scene
    else:
        mselList.add('*')
    
    # msellist iterator
    mselList_It = OpenMaya.MItSelectionList(mselList, OpenMaya.MFn.kTransform)
    
    transformReturn = []
    
    while not mselList_It.isDone():
        transform = mselList_It.getDagPath()
        transform_mfn = OpenMaya.MFnTransform(transform)

        for i in range(transform_mfn.attributeCount()):
            transform_attr = transform_mfn.attribute(i)  # MObject
            transform_plug = transform_mfn.findPlug(transform_attr, True).info  # conect a plug
            # fixme recollect float attributes, int, and boolean. better only boolean
            if transform_plug == '%s.%s' % (transform, attr) and transform_attr.apiType() == type:
                transformReturn.append(pm.PyNode(transform))
                break
        
        mselList_It.next()
    
    return transformReturn
    
    
def listAttrTypes():
    mSelList = OpenMaya.MGlobal.getActiveSelectionList()
    
    mSelIt = OpenMaya.MItSelectionList(mSelList)
    
    while not mSelIt.isDone():
        try:
            transform =  mSelIt.getDagPath()
            mfnTransform = OpenMaya.MFnTransform(transform)
        except:
            transform = mSelIt.getDependNode()
            mfnTransform = OpenMaya.MFnDependencyNode(transform)
            
        print transform
        
        for i in range(mfnTransform.attributeCount()):
            transformAttr = mfnTransform.attribute(i)
            transformAttr_plug = mfnTransform.findPlug(transformAttr, True)
            print ('%s is type: %s' % (transformAttr_plug.info, transformAttr.apiTypeStr))
            
        mSelIt.next()
    
    
def addAttribute():
    m_selectionList = OpenMaya.MGlobal.getActiveSelectionList()
    
    # mobject of first item of Mselection
    m_DepNode = m_selectionList.getDependNode(0)
    # set FnDependencyNode
    m_node_fn = OpenMaya.MFnDependencyNode(m_DepNode)
    
    #BoolAttribute
    fAttr = OpenMaya.MFnNumericAttribute()
    aSampleBool = fAttr.create('SampleBool', 'sb', OpenMaya.MFnNumericData.kBoolean, True) # get an mObject atttr
    
    fAttr.keyable = True
    fAttr.storable = True
    fAttr.readable = True
    fAttr.writable = True
    
    #StringAttribute
    fAttr = OpenMaya.MFnTypedAttribute()
    aSampleText = fAttr.create('sampleTXT', 'st', OpenMaya.MFnData.kString)
    

    fAttr.keyable = True
    fAttr.storable = True
    fAttr.readable = True
    fAttr.writable = True
    
    #multi Compound Attribute
    fAttr =  OpenMaya.MFnCompoundAttribute()
    aCompound = fAttr.create('sampleCompound', 'sc')
    fAttr.addChild(aSampleBool)
    fAttr.addChild(aSampleText)
    
    # fAttr.array = True  # this create a way to duplicate the attr multiple times
    fAttr.keyable = True
    fAttr.storable = True
    fAttr.readable = True
    fAttr.writable = True
    
    m_node_fn.addAttribute(aCompound)
    
def removeAttr(atributes=('exp'), *items):
    """
    this method search the attributes on the denamded items.
    Args:
        items(str): list of str or pynode we want to remove attr

    Returns: recalculate the list
    """
    for item in items:
        # check if item is pynode
        if not isinstance(item, pm.nodetypes.Transform):
            logger.debug('Create Pynode: %s, %s' % (item, type(item)))
            item = pm.PyNode(item)

        # deleteAttrs
        for attr in atributes:
            try:
                item.attr(attr).delete()
                logger.info('Remove attribute: %s.%s' % (item, attr))

            except:
                logger.info('Can not delete attr: %s' % attr)
