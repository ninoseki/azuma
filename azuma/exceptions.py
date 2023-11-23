class AzumaError(Exception):
    pass


class UnsupportedFeatureError(AzumaError):
    """Raised when a signature using an unsupported sigma feature is loaded."""

    pass


class RuleLoadError(AzumaError):
    pass
