import os


class QueryExpansion:
    def __init__(self, synonyms_file=None):
        """
        Initialize Query Expansion
        
        Args:
            synonyms_file: path to file containing synonyms (optional)
        """
        self.synonyms = {}  # term -> list of synonyms
        self.term_weights = {}  # term -> weight multiplier
        
        if synonyms_file and os.path.exists(synonyms_file):
            self.load_synonyms(synonyms_file)
    
    def load_synonyms(self, synonyms_file):
        """
        Load synonyms from file
        Format: term\tsynonym1,synonym2,synonym3
        """
        try:
            with open(synonyms_file, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) >= 2:
                        term = parts[0].lower()
                        synonyms = [s.strip().lower() for s in parts[1].split(',')]
                        self.synonyms[term] = synonyms
            print(f"Loaded {len(self.synonyms)} terms with synonyms")
            return True
        except Exception as e:
            print(f"Error loading synonyms: {e}")
            return False
    
    def add_synonyms(self, term, synonyms):
        """Add synonyms for a term"""
        term = term.lower()
        self.synonyms[term] = [s.lower() for s in synonyms]
    
    def expand_with_synonyms(self, query_tokens):
        """
        Expand query by adding synonyms of query terms
        
        Args:
            query_tokens: list of query tokens
            
        Returns:
            expanded query tokens (including original terms)
        """
        expanded = list(query_tokens)
        
        for term in query_tokens:
            if term in self.synonyms:
                expanded.extend(self.synonyms[term])
        
        return expanded
    
    def set_term_weights(self, term, weight):
        """
        Set weight multiplier for a term (boost certain terms)
        
        Args:
            term: the term to weight
            weight: weight multiplier (> 1 means boost)
        """
        self.term_weights[term.lower()] = weight
    
    def expand_with_weights(self, query_vector):
        """
        Expand query by boosting weights of important terms
        
        Args:
            query_vector: dict of {term: tfidf_value}
            
        Returns:
            expanded query vector with boosted weights
        """
        expanded_vector = query_vector.copy()
        
        for term, weight in self.term_weights.items():
            if term in expanded_vector:
                expanded_vector[term] *= weight
        
        return expanded_vector
    
    def create_default_synonyms(self):
        """Create a default set of domain-specific synonyms"""
        default_synonyms = {
            'weather': ['climate', 'temperature', 'condition'],
            'temperature': ['heat', 'cold', 'warm'],
            'rain': ['precipitation', 'rainfall', 'wet'],
            'snow': ['snowfall', 'snowstorm', 'blizzard'],
            'sun': ['sunny', 'bright', 'clear'],
            'wind': ['breeze', 'gust', 'storm'],
            'beach': ['shore', 'coast', 'seaside'],
            'outdoor': ['outside', 'outdoors', 'exterior'],
            'activity': ['activity', 'action', 'sport'],
            'enjoy': ['like', 'love', 'appreciate'],
            'plan': ['schedule', 'arrange', 'organize'],
            'relax': ['rest', 'relieve', 'unwind'],
            'season': ['period', 'time', 'quarter'],
            'change': ['alter', 'modify', 'transform'],
            'predict': ['forecast', 'prognosticate', 'anticipate'],
            'meteorologist': ['weather forecaster', 'meteorology expert'],
            'unpredictable': ['erratic', 'unstable', 'variable']
        }
        
        self.synonyms = default_synonyms
        return default_synonyms
    
    def save_synonyms(self, output_file):
        """Save synonyms to file"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for term in sorted(self.synonyms.keys()):
                    synonyms_str = ','.join(self.synonyms[term])
                    f.write(f"{term}\t{synonyms_str}\n")
            print(f"Synonyms saved to {output_file}")
            return True
        except Exception as e:
            print(f"Error saving synonyms: {e}")
            return False
