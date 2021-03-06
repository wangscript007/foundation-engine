# --------------------------------------------------
# Foundation Libs
import FoundationPython as Foundation
import Entity
from EntityWeapon import *
from log.HTTPLogger import *

# --------------------------------------------------
# Python Libs
import yaml
import random


class EntityManager(object):
    def __init__(self, _sEntityTypeFilename, _sWeaponTypeFilename):
        self.m_uManager = Foundation.EntityManager();
        self.Task = Foundation.Task(self, "doTask")
        self.EntityTypes = None
        self.WeaponTypes = None
        self.__readEntityTypesFromYaml(_sEntityTypeFilename)
        self.__readWeaponTypesFromYaml(_sWeaponTypeFilename)
        self.m_uEntityList = []

    def doTask(self, _nDeltaTime):
        for uEntity in self.m_uEntityList:
            uEntity.doTask(_nDeltaTime)

            # Check if the entity is done creating a unit
            uUnitType = uEntity.updateUnitCreation(_nDeltaTime)
            if (uUnitType != None):
                uEntityNew = self.addEntity("RANDOM_NAME_HERE_FIXME", uUnitType)
                uEntityNew.createGraphic("SceneManager0")
                uEntityNew.createCollision(Foundation.CollisionShapeId.BOX, Foundation.Vector3(1, 1, 1))
                uEntityNew.setPosition(Foundation.Vector3(30, 20, 30))
                uEntityNew.moveTo(Foundation.Vector3(random.randrange(-500, 500, 1), 20, random.randrange(-500, 500, 1)))

                HTTPLogger().writeContent(LoggerError.NONE, "Entity type %s created by %s" % (uUnitType["Name"], uEntity.getName()))

    def addEntity(self, _sName, _uType):
        if not self.hasEntityType(_uType["Name"]):
            self.m_uLogger.writeContent(LoggerError.ERROR, "[EntityManager] EntityType " + _sType + " doesn't exist.")
            return None
        else:
            entDerived = Entity.Entity(self.m_uManager.addEntity(_sName))
            entDerived.setType(_uType)

            # Attach all weapon types
            if (_uType["Weapons"]):
                for sWeaponName in _uType["Weapons"]:
                    uWeaponType = self.WeaponTypes[sWeaponName]

                    uWeapon = EntityWeapon()
                    uWeapon.setup(uWeaponType["Name"], uWeaponType["Power"], uWeaponType["Speed"], uWeaponType["RangeMin"], uWeaponType["RangeMax"], uWeaponType["Cooldown"], uWeaponType["FrontalArc"])
                    entDerived.attachWeapon(uWeapon)

            self.m_uEntityList.append(entDerived)
            HTTPLogger().writeContent(LoggerError.NONE, "[EntityManager] Created Entity of Type %s" % (_uType["Name"]))

            return entDerived

    # This is used by the API for ingame unit creation
    def createEntity(self, _uConstructingEntity, _uType):
        if (_uConstructingEntity != None):
            _uConstructingEntity.createUnit(_uType)

    # --------------------------------------
    # Entity API
    def getEntityByName(self, _sName):
        for uEntity in self.m_uEntityList:
            if uEntity.getName() == _sName:
                return uEntity
        return None

    def getEntityById(self, _nId):
        for uEntity in self.m_uEntityList:
            if uEntity.getId() == _nId:
                return uEntity
        return None

    def getEntityTypes(self):
        return self.EntityTypes

    def getEntityTypeFromName(self, _sName):
        for sUnit in self.EntityTypes:
            if sUnit == _sName:
                return self.EntityTypes[sUnit]

    def hasEntityType(self, _sType):
        if self.EntityTypes:
            return _sType in self.EntityTypes
        return None

    # --------------------------------------
    # Weapon API
    def getWeaponByName(self, _sName):
        for uWeapon in self.m_uWeaponList:
            if uWeapon.getName() == _sName:
                return uWeapon
        return None

    def getWeaponById(self, _nId):
        for uWeapon in self.m_uWeaponList:
            if uWeapon.getId() == _nId:
                return uWeapon
        return None

    def getWeaponTypes(self):
        return self.WeaponTypes

    def getWeaponTypeFromName(self, _sName):
        for sUnit in self.WeaponTypes:
            if sUnit == _sName:
                return self.WeaponTypes[sUnit]

    def hasWeaponType(self, _sType):
        if self.WeaponTypes:
            return _sType in self.WeaponTypes
        return None

    # Private methods
    def __readEntityTypesFromYaml(self, _sFilename):
        # Load entityTypes from a YAML file
        stream = file(_sFilename, 'r')
        self.EntityTypes = yaml.load(stream)['EntityTypes']

    def __readWeaponTypesFromYaml(self, _sFilename):
        # Load entityTypes from a YAML file
        stream = file(_sFilename, 'r')
        self.WeaponTypes = yaml.load(stream)['WeaponTypes']

