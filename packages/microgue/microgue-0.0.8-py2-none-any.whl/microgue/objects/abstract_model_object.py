from ..models.abstract_model import DeleteFailed
from .object import Object


class RequiredAttributes(Exception):
    pass


class AbstractModelObject(Object):
    """
    attributes: defined on Object
    protected_attributes: defined on Object

    required_attributes: attributes that must be include when creating a new object in the database

    _model: the instantiated model that AbstractModelObject will use to connect to the database
    """
    required_attributes = []
    _model = None

    def __init__(self, attributes_or_pk_value={}, sk_value=None):
        if type(attributes_or_pk_value) is dict:
            super().__init__(attributes_or_pk_value)
        elif type(attributes_or_pk_value) is str:
            super().__init__(self._model.get(attributes_or_pk_value, sk_value))

    def insert(self):
        missing_required_attributes = self._get_missing_required_attributes()
        if missing_required_attributes:
            raise RequiredAttributes('missing the following required attributes: ' + ', '.join(missing_required_attributes))
        self.deserialize(self._model.insert(self.serialize(hide_protected_attributes=False)))

    def update(self):
        self.deserialize(self._model.update(self.serialize(hide_protected_attributes=False)))

    def save(self):
        # get pk and sk
        pk = self.__dict__.get(self._model.pk, None)
        sk = self.__dict__.get(self._model.pk, None)

        # check if the record exists
        try:
            record_exists = bool(self._model.get(pk, sk))
        except:
            record_exists = False

        # call update or insert accordingly
        if record_exists:
            self.update()
        else:
            self.insert()

    def delete(self):
        # get pk and sk
        pk = self.__dict__.get(self._model.pk, None)
        sk = self.__dict__.get(self._model.pk, None)

        try:
            return self._model.delete(pk, sk)
        except Exception as e:
            raise DeleteFailed(str(e))

    def _get_missing_required_attributes(self):
        missing_required_attributes = []
        for required_attribute in self.required_attributes:
            if self.__dict__.get(required_attribute, None) is None:
                missing_required_attributes.append(required_attribute)
        return missing_required_attributes
