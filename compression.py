import struct


class IndexCompression:
    @staticmethod
    def gap_encode(doc_ids):
        """
        Gap Encoding: Store differences between consecutive docIDs instead of actual IDs
        
        Args:
            doc_ids: sorted list or set of docIDs (strings like 'Doc1', 'Doc2', etc.)
            
        Returns:
            list of gap values
        """
        # Convert docID strings to numbers for gap encoding
        # Extract numbers from docID strings
        sorted_ids = sorted(doc_ids, key=lambda x: int(x.replace('Doc', '')))
        
        if not sorted_ids:
            return []
        
        # Convert to numeric IDs
        numeric_ids = [int(doc_id.replace('Doc', '')) for doc_id in sorted_ids]
        
        gaps = []
        gaps.append(numeric_ids[0])  # First value
        
        for i in range(1, len(numeric_ids)):
            gap = numeric_ids[i] - numeric_ids[i-1]
            gaps.append(gap)
        
        return gaps
    
    @staticmethod
    def gap_decode(gaps):
        """
        Gap Decoding: Reconstruct docIDs from gap values
        
        Args:
            gaps: list of gap values
            
        Returns:
            list of docID strings
        """
        if not gaps:
            return []
        
        numeric_ids = []
        numeric_ids.append(gaps[0])
        
        for i in range(1, len(gaps)):
            numeric_ids.append(numeric_ids[i-1] + gaps[i])
        
        # Convert back to docID strings
        doc_ids = [f'Doc{doc_id}' for doc_id in numeric_ids]
        return doc_ids
    
    @staticmethod
    def compress_index(inverted_index):
        """
        Compress entire inverted index using gap encoding
        
        Args:
            inverted_index: dict of {term: set(docIDs)}
            
        Returns:
            dict of {term: compressed_gaps}
        """
        compressed = {}
        
        for term, doc_ids in inverted_index.items():
            compressed[term] = IndexCompression.gap_encode(doc_ids)
        
        return compressed
    
    @staticmethod
    def decompress_index(compressed_index):
        """
        Decompress entire inverted index from gap encoding
        
        Args:
            compressed_index: dict of {term: compressed_gaps}
            
        Returns:
            dict of {term: set(docIDs)}
        """
        decompressed = {}
        
        for term, gaps in compressed_index.items():
            decompressed[term] = set(IndexCompression.gap_decode(gaps))
        
        return decompressed
    
    @staticmethod
    def save_compressed_index(compressed_index, output_file):
        """Save compressed index to file"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for term in sorted(compressed_index.keys()):
                    gaps = compressed_index[term]
                    gaps_str = ','.join(str(g) for g in gaps)
                    f.write(f"{term}\t{gaps_str}\n")
            print(f"Compressed index saved to {output_file}")
            return True
        except Exception as e:
            print(f"Error saving compressed index: {e}")
            return False
    
    @staticmethod
    def load_compressed_index(input_file):
        """Load compressed index from file"""
        try:
            compressed = {}
            with open(input_file, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) >= 2:
                        term = parts[0]
                        gaps = [int(g) for g in parts[1].split(',')]
                        compressed[term] = gaps
            print(f"Compressed index loaded from {input_file}")
            return compressed
        except Exception as e:
            print(f"Error loading compressed index: {e}")
            return None
    
    @staticmethod
    def get_compression_ratio(original_index, compressed_index):
        """Calculate compression ratio"""
        original_size = sum(len(ids) for ids in original_index.values())
        compressed_size = sum(len(gaps) for gaps in compressed_index.values())
        
        ratio = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0
        return ratio
