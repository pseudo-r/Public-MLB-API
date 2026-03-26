"""Database models for MLB Stats data."""

from django.db import models


class TimestampMixin(models.Model):
    """Mixin providing created_at and updated_at timestamps."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Venue(TimestampMixin):
    """MLB stadium / venue."""

    mlb_id = models.PositiveIntegerField(unique=True, db_index=True)
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True, default="USA")
    capacity = models.PositiveIntegerField(null=True, blank=True)
    roof_type = models.CharField(max_length=50, blank=True)  # e.g., "Open", "Dome", "Retractable"
    turf_type = models.CharField(max_length=50, blank=True)  # e.g., "Grass", "AstroTurf 3D"
    left_line = models.PositiveIntegerField(null=True, blank=True)  # feet
    left_center = models.PositiveIntegerField(null=True, blank=True)
    center = models.PositiveIntegerField(null=True, blank=True)
    right_center = models.PositiveIntegerField(null=True, blank=True)
    right_line = models.PositiveIntegerField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    active = models.BooleanField(default=True)
    raw_data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        location = ", ".join(filter(None, [self.city, self.state]))
        return f"{self.name} ({location})" if location else self.name


class Team(TimestampMixin):
    """MLB team."""

    mlb_id = models.PositiveIntegerField(unique=True, db_index=True)
    name = models.CharField(max_length=100)  # full name, e.g., "Los Angeles Dodgers"
    team_name = models.CharField(max_length=50, blank=True)  # e.g., "Dodgers"
    location_name = models.CharField(max_length=100, blank=True)  # e.g., "Los Angeles"
    abbreviation = models.CharField(max_length=10, db_index=True)
    team_code = models.CharField(max_length=10, blank=True)  # e.g., "lan"
    file_code = models.CharField(max_length=10, blank=True)  # e.g., "la"
    league_id = models.PositiveIntegerField(null=True, blank=True)  # 103=AL, 104=NL
    league_name = models.CharField(max_length=50, blank=True)
    division_id = models.PositiveIntegerField(null=True, blank=True)
    division_name = models.CharField(max_length=50, blank=True)
    sport_id = models.PositiveIntegerField(default=1)  # 1=MLB
    venue = models.ForeignKey(
        Venue,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="teams",
    )
    first_year_of_play = models.CharField(max_length=4, blank=True)
    active = models.BooleanField(default=True, db_index=True)
    raw_data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.abbreviation})"


class Player(TimestampMixin):
    """MLB player / person."""

    mlb_id = models.PositiveIntegerField(unique=True, db_index=True)
    full_name = models.CharField(max_length=150, db_index=True)
    first_name = models.CharField(max_length=75, blank=True)
    last_name = models.CharField(max_length=75, blank=True)
    primary_number = models.CharField(max_length=5, blank=True)  # jersey #
    birth_date = models.DateField(null=True, blank=True)
    birth_city = models.CharField(max_length=100, blank=True)
    birth_country = models.CharField(max_length=100, blank=True)
    height = models.CharField(max_length=10, blank=True)  # e.g., "6' 4\""
    weight = models.PositiveIntegerField(null=True, blank=True)  # lbs

    # Position
    position = models.CharField(max_length=50, blank=True)  # e.g., "Pitcher"
    position_abbreviation = models.CharField(max_length=5, blank=True)  # e.g., "SP"
    position_type = models.CharField(max_length=20, blank=True)  # e.g., "Starter"

    # Handedness
    SIDE_CHOICES = [("L", "Left"), ("R", "Right"), ("S", "Switch")]
    bat_side = models.CharField(max_length=1, choices=SIDE_CHOICES, blank=True)
    pitch_hand = models.CharField(max_length=1, choices=SIDE_CHOICES, blank=True)

    # Current team association (nullable — players can be free agents / retired)
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="players",
    )

    active = models.BooleanField(default=True, db_index=True)
    mlb_debut_date = models.DateField(null=True, blank=True)
    last_played_date = models.DateField(null=True, blank=True)

    # Media
    headshot_url = models.URLField(max_length=500, blank=True)

    raw_data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self) -> str:
        team_abbr = self.team.abbreviation if self.team else "FA"
        return f"{self.full_name} ({team_abbr}, #{self.primary_number})"


class Game(TimestampMixin):
    """MLB game (schedule entry + live/final state)."""

    mlb_pk = models.PositiveIntegerField(unique=True, db_index=True)
    game_date = models.DateTimeField(db_index=True)
    official_date = models.DateField(db_index=True, null=True, blank=True)

    # Game metadata
    GAME_TYPE_CHOICES = [
        ("S", "Spring Training"),
        ("E", "Exhibition"),
        ("R", "Regular Season"),
        ("F", "Wild Card"),
        ("D", "Division Series"),
        ("L", "League Championship"),
        ("W", "World Series"),
    ]
    game_type = models.CharField(max_length=2, choices=GAME_TYPE_CHOICES, default="R")
    season = models.PositiveIntegerField(db_index=True)
    series_description = models.CharField(max_length=100, blank=True)

    # Teams
    home_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="home_games"
    )
    away_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="away_games"
    )
    venue = models.ForeignKey(
        Venue, on_delete=models.SET_NULL, null=True, blank=True, related_name="games"
    )

    # Status
    STATUS_SCHEDULED = "scheduled"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_FINAL = "final"
    STATUS_POSTPONED = "postponed"
    STATUS_SUSPENDED = "suspended"
    STATUS_CANCELLED = "cancelled"
    STATUS_CHOICES = [
        (STATUS_SCHEDULED, "Scheduled"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_FINAL, "Final"),
        (STATUS_POSTPONED, "Postponed"),
        (STATUS_SUSPENDED, "Suspended"),
        (STATUS_CANCELLED, "Cancelled"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_SCHEDULED, db_index=True)
    detailed_state = models.CharField(max_length=50, blank=True)

    # Scores
    home_score = models.PositiveSmallIntegerField(null=True, blank=True)
    away_score = models.PositiveSmallIntegerField(null=True, blank=True)

    # Inning info (live + final)
    current_inning = models.PositiveSmallIntegerField(null=True, blank=True)
    inning_state = models.CharField(max_length=10, blank=True)  # "Top", "Bottom", "End"

    # Doubleheader
    double_header = models.CharField(max_length=1, blank=True)  # "Y", "N", "S"
    game_number = models.PositiveSmallIntegerField(default=1)

    raw_data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-game_date"]

    def __str__(self) -> str:
        date_str = self.official_date.isoformat() if self.official_date else "?"
        return f"{self.away_team.abbreviation} @ {self.home_team.abbreviation} ({date_str})"

    @property
    def final_score(self) -> str:
        if self.home_score is not None and self.away_score is not None:
            return f"{self.away_score}-{self.home_score}"
        return "–"


class Standing(TimestampMixin):
    """Division standing for a team in a given season."""

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="standings",
    )
    season = models.PositiveIntegerField(db_index=True)
    standings_type = models.CharField(max_length=30, default="regularSeason", db_index=True)

    # League / division context
    league_id = models.PositiveIntegerField()
    division_id = models.PositiveIntegerField()
    division_rank = models.PositiveSmallIntegerField(null=True, blank=True)
    league_rank = models.PositiveSmallIntegerField(null=True, blank=True)
    wild_card_rank = models.PositiveSmallIntegerField(null=True, blank=True)
    sport_rank = models.PositiveSmallIntegerField(null=True, blank=True)

    # Win/loss record
    wins = models.PositiveSmallIntegerField(default=0)
    losses = models.PositiveSmallIntegerField(default=0)
    pct = models.CharField(max_length=6, blank=True)  # ".600"
    games_back = models.CharField(max_length=10, blank=True)  # "-", "1.5"
    wild_card_games_back = models.CharField(max_length=10, blank=True)

    # Streaks
    streak_code = models.CharField(max_length=10, blank=True)  # e.g., "W3"
    last_ten = models.CharField(max_length=10, blank=True)  # e.g., "7-3"

    clinched = models.BooleanField(default=False)

    raw_data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["division_rank"]
        unique_together = [["team", "season", "standings_type"]]

    def __str__(self) -> str:
        return f"{self.team.abbreviation} — {self.season} ({self.wins}-{self.losses})"


class Transaction(TimestampMixin):
    """MLB player transaction (trade, signing, IL move, DFA, etc.)."""

    mlb_id = models.CharField(max_length=50, blank=True, db_index=True)

    # Player
    person_name = models.CharField(max_length=150, blank=True)
    person_mlb_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)

    # Teams
    to_team = models.ForeignKey(
        Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="incoming_transactions"
    )
    from_team = models.ForeignKey(
        Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="outgoing_transactions"
    )

    # Dates
    date = models.DateField(null=True, blank=True, db_index=True)
    effective_date = models.DateField(null=True, blank=True)
    resolution_date = models.DateField(null=True, blank=True)

    # Type
    type_code = models.CharField(max_length=10, blank=True)  # e.g., "TR", "SG", "DFA"
    type_desc = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    raw_data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-date", "-updated_at"]

    def __str__(self) -> str:
        return f"{self.person_name} — {self.type_desc} ({self.date})"
