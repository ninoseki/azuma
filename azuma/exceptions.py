class AzumaError(Exception):
    pass


class UnsupportedFeature(AzumaError):
    """Raised when a signature using an unsupported sigma feature is loaded."""

    pass


class RuleLoadError(AzumaError):
    pass
