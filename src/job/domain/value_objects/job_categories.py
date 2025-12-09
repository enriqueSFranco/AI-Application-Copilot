from enum import Enum


class JobCategory(Enum):
    # --- Desarrollo de Software ---
    SOFTWARE_ENGINEERING = "Ingeniería de Software"
    FRONTEND_DEVELOPMENT = "Desarrollo Frontend"
    BACKEND_DEVELOPMENT = "Desarrollo Backend"
    FULLSTACK_DEVELOPMENT = "Desarrollo Full-Stack"
    MOBILE_DEVELOPMENT = "Desarrollo Móvil"
    GAME_DEVELOPMENT = "Desarrollo de Videojuegos"
    EMBEDDED_SYSTEMS = "Sistemas Embebidos"
    ERP_DEVELOPMENT = "Desarrollo ERP / SAP"
    BLOCKCHAIN = "Blockchain / Web3"

    # --- Infraestructura y Operaciones ---
    DEVOPS = "DevOps"
    CLOUD_ENGINEERING = "Ingeniería de la Nube"
    SITE_RELIABILITY_ENGINEERING = "Ingeniería de Confiabilidad (SRE)"
    NETWORK_ENGINEERING = "Ingeniería de Redes"
    IT_SUPPORT = "Soporte TI"
    HARDWARE_ENGINEERING = "Ingeniería de Hardware"

    # --- Datos e Inteligencia Artificial ---
    DATA_SCIENCE = "Ciencia de Datos"
    DATA_ANALYTICS = "Análisis de Datos"
    AI_ML_ENGINEERING = "Ingeniería de IA / Machine Learning"
    DATABASE_ADMINISTRATION = "Administración de Bases de Datos"

    # --- Gestión y Análisis de Negocio ---
    PROJECT_MANAGEMENT = "Gestión de Proyectos"
    PRODUCT_MANAGEMENT = "Gestión de Producto"
    BUSINESS_ANALYSIS = "Análisis de Negocio"

    # --- Seguridad y Cumplimiento ---
    CYBERSECURITY = "Ciberseguridad"
    IT_AUDIT_COMPLIANCE = "Auditoría y Cumplimiento TI"

    # --- Calidad, UX y Documentación ---
    QA_TESTING = "QA / Testing"
    UX_UI_DESIGN = "Diseño UX/UI"
    TECHNICAL_WRITING = "Documentación Técnica"

    # --- Automatización ---
    RPA_AUTOMATION = "Automatización / RPA"

    # --- Arquitectura ---
    ENTERPRISE_ARCHITECTURE = "Arquitectura Empresarial"


JOB_LABELS = [category.value for category in JobCategory]
