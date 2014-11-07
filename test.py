import pkmn_test
import extract_feats

# Test feature extraction on a random team
team = pkmn_test.random_Team()
tmext = extract_feats.teamExtractor(team, prefix='')
tmext.extract()
feats = tmext.getFeats()
print 'Basic Extraction'
print len(feats.keys())
    
# Test more battlee feature extraction
team.init_battle({'Level':'As Is'}) # Fake battle vals
tmext = extract_feats.teamExtractor(team, True, prefix='1')
tmext.extract()
feats = tmext.getFeats()
print '\n\nAdvanced Extraction'
print len(feats.keys())
items = feats.items()
items.sort()
for item in items:
    print item