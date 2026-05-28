from modules.vacancies.domain.ports.vacancy_repository_port import VacancyRepositoryPort


class VacancyService:
    def __init__(
        self, repo: VacancyRepositoryPort, embeddings_client, classifier, risk_client
    ):
        self.repo = repo
        self.embeddings_client = embeddings_client
        self.classifier = classifier
        self.risk_client = risk_client

    # Toma el raw scraped payload, crea Vacancy, lanza pipeline IA y persiste.
    def create_from_scrape(self):
        pass

    def update_and_detect_changes(self):
        pass

    # compara campos clave y solo rerun pipeline si hay cambios importantes.
    def _detect_changes(self):
        pass

    # Orquesta calls a ClassifierClient, EmbeddingsClient, RiskClient.
    # NOTE: En producción estos deben ser adaptadores que implementen timeouts, retries y circuit breakers.
    async def _run_ai_pipeline(self):
        pass

    def _compute_priority(self):
        pass
