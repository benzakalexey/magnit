from classic.app import validate_with_dto
from classic.components import component
from pydantic import validate_arguments, conint

from magnit.application import interfaces, entities, errors, dtos_layer
from magnit.application.services.join_point import join_point


@component
class DocLog:
    """
    Класс Логи документов
    """
    docs_log_repo: interfaces.DocLogRepo
    users_repo: interfaces.UserRepo
    visits_repo: interfaces.VisitRepo

    @join_point
    @validate_arguments
    def get_by_id(self, doc_log_id: conint(gt=0)) -> entities.DocsLog:
        doc_log = self.docs_log_repo.get_by_id(doc_log_id)
        if doc_log is None:
            raise errors.DocLogIDNotExistError(doc_log_id=doc_log_id)

        return doc_log

    @join_point
    def get_all(self):
        return self.docs_log_repo.get_all()

    @join_point
    @validate_with_dto
    def add_doc_log(self, docs_log_info: dtos_layer.DocLogInfo):
        user = self.users_repo.get_by_id(docs_log_info.user_id)
        if user is None:
            raise errors.UserIDNotExistError(user_id=docs_log_info.user_id)

        visit = self.visits_repo.get_by_id(docs_log_info.visit_id)
        if visit is None:
            raise errors.VisitIDNotExistError(visit_id=docs_log_info.visit_id)

        doc_log = entities.DocsLog(
            visit=visit,
            user=user,
            doc_type=docs_log_info.doc_type,
            doc_name=docs_log_info.doc_name
        )
        self.docs_log_repo.add(doc_log)
        self.docs_log_repo.save()
