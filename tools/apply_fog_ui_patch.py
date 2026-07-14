from pathlib import Path
from textwrap import dedent


def replace_once(path: str, old: str, new: str) -> None:
    file = Path(path)
    text = file.read_text()
    if old not in text:
        raise RuntimeError(f"Expected source block not found in {path}: {old[:120]!r}")
    file.write_text(text.replace(old, new, 1))


def replace_between(path: str, start_marker: str, end_marker: str, replacement: str) -> None:
    file = Path(path)
    text = file.read_text()
    start = text.index(start_marker)
    end = text.index(end_marker, start)
    file.write_text(text[:start] + replacement + text[end:])


tile = "game-app/game-core/src/main/java/games/strategy/triplea/ui/screen/TileManager.java"
replace_once(
    tile,
    "import games.strategy.triplea.ui.mapdata.MapData;\n",
    "import games.strategy.triplea.ui.mapdata.MapData;\n"
    "import games.strategy.triplea.ui.visibility.LocalPlayerVisibility;\n",
)
replace_once(
    tile,
    "import games.strategy.triplea.ui.screen.drawable.DecoratorDrawable;\n",
    "import games.strategy.triplea.ui.screen.drawable.DecoratorDrawable;\n"
    "import games.strategy.triplea.ui.screen.drawable.FogOfWarDrawable;\n",
)
replace_once(tile, "import java.util.Set;\n", "import java.util.Set;\nimport java.util.stream.Collectors;\n")
replace_once(
    tile,
    "  private final Collection<UnitsDrawer> allUnitDrawables = new ArrayList<>();\n"
    "  private final UiContext uiContext;\n",
    "  private final Collection<UnitsDrawer> allUnitDrawables = new ArrayList<>();\n"
    "  private volatile Set<String> visibleTerritoryNames = Set.of();\n"
    "  private volatile boolean fogOfWarMasking;\n"
    "  private final UiContext uiContext;\n",
)
replace_once(
    tile,
    "  public TileManager(final UiContext uiContext) {\n"
    "    this.uiContext = uiContext;\n"
    "  }\n",
    dedent(
        """\
          public TileManager(final UiContext uiContext) {
            this.uiContext = uiContext;
          }

          public boolean isTerritoryVisible(final Territory territory) {
            return !fogOfWarMasking || visibleTerritoryNames.contains(territory.getName());
          }

          public boolean isFogOfWarMasking() {
            return fogOfWarMasking;
          }

          private boolean refreshVisibility(final GameState data) {
            final boolean updatedMasking = LocalPlayerVisibility.isMaskingEnabled(uiContext, data);
            final Set<String> updatedNames =
                updatedMasking
                    ? LocalPlayerVisibility.getVisibleTerritories(uiContext, data).stream()
                        .map(Territory::getName)
                        .collect(Collectors.toUnmodifiableSet())
                    : Set.of();
            final boolean changed =
                updatedMasking != fogOfWarMasking || !updatedNames.equals(visibleTerritoryNames);
            fogOfWarMasking = updatedMasking;
            visibleTerritoryNames = updatedNames;
            return changed;
          }
        """
    ),
)
replace_once(
    tile,
    "  public void resetTiles(final GameData data, final MapData mapData) {\n"
    "    try (GameData.Unlocker ignored = data.acquireReadLock()) {\n",
    "  public void resetTiles(final GameData data, final MapData mapData) {\n"
    "    refreshVisibility(data);\n"
    "    try (GameData.Unlocker ignored = data.acquireReadLock()) {\n",
)
replace_once(
    tile,
    "  public void updateTerritories(\n"
    "      final Collection<Territory> territories, final GameData data, final MapData mapData) {\n"
    "    try (GameData.Unlocker ignored = data.acquireReadLock()) {\n"
    "      synchronized (mutex) {\n"
    "        for (final Territory territory : territories) {\n"
    "          updateTerritory(territory, data, mapData);\n"
    "        }\n"
    "      }\n"
    "    }\n"
    "  }\n",
    dedent(
        """\
          public void updateTerritories(
              final Collection<Territory> territories, final GameData data, final MapData mapData) {
            final boolean visibilityChanged = refreshVisibility(data);
            final Collection<Territory> territoriesToUpdate =
                visibilityChanged ? data.getMap().getTerritories() : territories;
            try (GameData.Unlocker ignored = data.acquireReadLock()) {
              synchronized (mutex) {
                for (final Territory territory : territoriesToUpdate) {
                  updateTerritory(territory, data, mapData);
                }
              }
            }
          }
        """
    ),
)
new_draw_territory = dedent(
    """\
      private void drawTerritory(
          @Nonnull final Territory territory, final GameState data, final MapData mapData) {
        final Set<Tile> drawnOn = new HashSet<>();
        final Set<IDrawable> drawing = new HashSet<>();
        final boolean visible = isTerritoryVisible(territory);
        if (visible && territoryOverlays.get(territory.getName()) != null) {
          drawing.add(territoryOverlays.get(territory.getName()));
        }
        if (visible && uiContext.getShowTerritoryEffects()) {
          drawTerritoryEffects(territory, mapData, drawing);
        }
        if (visible && uiContext.getShowUnits()) {
          drawUnits(territory, mapData, drawnOn, drawing);
        }
        if (visible) {
          drawing.add(new BattleDrawable(territory.getName()));
        }
        final Optional<TerritoryAttachment> optionalTerritoryAttachment =
            TerritoryAttachment.get(territory);
        if (!territory.isWater()) {
          if (visible) {
            drawing.add(new LandTerritoryDrawable(territory));
          }
        } else {
          if (visible && optionalTerritoryAttachment.isPresent()) {
            final TerritoryAttachment ta = optionalTerritoryAttachment.get();
            if (ta.getKamikazeZone()) {
              drawing.add(new KamikazeZoneDrawable(territory, uiContext));
            }
            if (ta.getBlockadeZone()) {
              drawing.add(new BlockadeZoneDrawable(territory));
            }
            if (ta.getConvoyRoute() || ta.getProduction() > 0) {
              drawing.add(new ConvoyZoneDrawable(territory.getOwner(), territory, uiContext));
            }
          }
          drawing.add(new SeaZoneOutlineDrawable(territory.getName()));
        }
        if (!visible) {
          drawing.add(new FogOfWarDrawable(territory));
        }
        drawing.add(new TerritoryNameDrawable(territory.getName(), uiContext));
        if (visible
            && optionalTerritoryAttachment.map(TerritoryAttachment::isCapital).orElse(false)
            && mapData.drawCapitolMarkers()) {
          final GamePlayer capitalOf =
              data.getPlayerList().getPlayerId(optionalTerritoryAttachment.get().getCapitalOrThrow());
          drawing.add(new CapitolMarkerDrawable(capitalOf, territory, uiContext));
        }
        if (visible
            && optionalTerritoryAttachment.map(TerritoryAttachment::getVictoryCity).orElse(0) != 0) {
          drawing.add(new VcDrawable(territory));
        }
        for (final Tile tile : getTiles(mapData.getBoundingRect(territory.getName()))) {
          drawnOn.add(tile);
          tile.addDrawables(drawing);
        }
        territoryDrawables.put(territory.getName(), drawing);
        territoryTiles.put(territory.getName(), drawnOn);
      }
    """
)
replace_between(
    tile,
    "  private void drawTerritory(\n",
    "\n  private static void drawTerritoryEffects(",
    new_draw_territory,
)

small = "game-app/game-core/src/main/java/games/strategy/triplea/ui/screen/SmallMapImageManager.java"
replace_once(
    small,
    "import games.strategy.triplea.ui.screen.drawable.LandTerritoryDrawable;\n",
    "import games.strategy.triplea.ui.screen.drawable.FogOfWarDrawable;\n"
    "import games.strategy.triplea.ui.screen.drawable.LandTerritoryDrawable;\n",
)
replace_once(
    small,
    "      new LandTerritoryDrawable(t)\n"
    "          .draw(bounds, g, mapData, mapData.getSmallMapTerritorySaturation());\n",
    "      if (tileManager.isTerritoryVisible(t)) {\n"
    "        new LandTerritoryDrawable(t)\n"
    "            .draw(bounds, g, mapData, mapData.getSmallMapTerritorySaturation());\n"
    "      } else {\n"
    "        new FogOfWarDrawable(t).draw(bounds, g, mapData);\n"
    "      }\n",
)

panel = "game-app/game-core/src/main/java/games/strategy/triplea/ui/panels/map/MapPanel.java"
replace_once(
    panel,
    "import games.strategy.triplea.delegate.Matches;\n",
    "import games.strategy.triplea.delegate.Matches;\n"
    "import games.strategy.triplea.delegate.visibility.VisibilityAudit;\n",
)
replace_once(
    panel,
    "import games.strategy.triplea.ui.screen.UnitsDrawer;\n",
    "import games.strategy.triplea.ui.screen.UnitsDrawer;\n"
    "import games.strategy.triplea.ui.visibility.LocalPlayerVisibility;\n",
)
replace_once(
    panel,
    "        public void ownerChanged(final Territory territory) {\n"
    "          smallMapImageManager.updateTerritoryOwner(territory, gameData, uiContext.getMapData());\n"
    "          updateCountries(Set.of(territory));\n"
    "        }\n",
    "        public void ownerChanged(final Territory territory) {\n"
    "          updateCountries(Set.of(territory));\n"
    "        }\n",
)
replace_once(
    panel,
    "            if (terr != null) {\n"
    "              notifyTerritorySelected(terr, md);\n"
    "            }\n",
    "            if (terr != null) {\n"
    "              if (!tileManager.isTerritoryVisible(terr)) {\n"
    "                VisibilityAudit.canReveal(\n"
    "                    \"map-territory-selection\",\n"
    "                    terr,\n"
    "                    LocalPlayerVisibility.getViewers(uiContext, gameData),\n"
    "                    gameData);\n"
    "              }\n"
    "              notifyTerritorySelected(terr, md);\n"
    "            }\n",
)
new_hover = dedent(
    """\
      private void updateMouseHoverState(final MouseDetails md, final int mouseX, final int mouseY) {
        final double scaledMouseX = mouseX / scale;
        final double scaledMouseY = mouseY / scale;
        final double x = normalizeX(scaledMouseX + getXOffset());
        final double y = normalizeY(scaledMouseY + getYOffset());
        final Territory territory = getTerritory(x, y);
        final boolean visible = territory == null || tileManager.isTerritoryVisible(territory);
        final Territory displayTerritory = visible ? territory : null;
        if (!Objects.equals(displayTerritory, currentTerritory)) {
          currentTerritory = displayTerritory;
          notifyMouseEntered(displayTerritory);
        }
        if (md != null) {
          notifyMouseMoved(displayTerritory, md);
        }
        final Tuple<Territory, List<Unit>> tuple =
            visible ? tileManager.getUnitsAtPoint(x, y, gameData) : null;
        if (unitsChanged(tuple)) {
          currentUnits = tuple;
          if (tuple == null) {
            notifyMouseEnterUnit(List.of(), displayTerritory);
          } else {
            notifyMouseEnterUnit(tuple.getSecond(), tuple.getFirst());
          }
        }
      }
    """
)
replace_between(
    panel,
    "  private void updateMouseHoverState(",
    "\n  private void recreateTiles(",
    new_hover,
)
replace_once(
    panel,
    "              tileManager.updateTerritories(toUpdate, gameData, uiContext.getMapData());\n"
    "              smallMapImageManager.update(uiContext.getMapData());\n",
    "              if (LocalPlayerVisibility.isMaskingEnabled(uiContext, gameData)) {\n"
    "                toUpdate = new ArrayList<>(gameData.getMap().getTerritories());\n"
    "              }\n"
    "              tileManager.updateTerritories(toUpdate, gameData, uiContext.getMapData());\n"
    "              for (final Territory territory : toUpdate) {\n"
    "                smallMapImageManager.updateTerritoryOwner(\n"
    "                    territory, gameData, uiContext.getMapData());\n"
    "              }\n"
    "              smallMapImageManager.update(uiContext.getMapData());\n",
)
replace_once(
    panel,
    "      executor.execute(() -> tileManager.resetTiles(gameData, uiContext.getMapData()));\n",
    "      executor.execute(\n"
    "          () -> {\n"
    "            tileManager.resetTiles(gameData, uiContext.getMapData());\n"
    "            initSmallMap();\n"
    "          });\n",
)
