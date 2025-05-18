import tkinter as tk
from tkinter import ttk, font, messagebox, scrolledtext
import re
from collections import defaultdict

class LexicalAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("C Code Analyzer")
        self.root.geometry("1000x800")
        self.root.configure(bg="#f0f0f0")
        
        # Configure window to be centered
        self.center_window()
        
        # Set up fonts
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=11)
        self.root.option_add("*Font", default_font)
        
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input section
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        input_label = ttk.Label(input_frame, text="Enter C code:")
        input_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Use scrolledtext for input
        self.input_text = scrolledtext.ScrolledText(input_frame, width=70, height=10)
        self.input_text.pack(fill=tk.X, ipady=5)
        self.input_text.insert("1.0", """#include <stdio.h>

int main() {
    int x = 5;
    if (x > 0) {
        printf("Positive number\\n");
    }
    return 0;
}""")
        
        # Button section
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        analyze_button = ttk.Button(button_frame, text="Analyze", command=self.analyze_text)
        analyze_button.pack(pady=10)
        
        # Output section
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for different analysis views
        self.notebook = ttk.Notebook(output_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Lexical Analysis Tab
        lexical_frame = ttk.Frame(self.notebook)
        self.notebook.add(lexical_frame, text="Lexical Analysis")
        
        lexical_label = ttk.Label(lexical_frame, text="Lexical Analysis Result:")
        lexical_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.lexical_text = scrolledtext.ScrolledText(
            lexical_frame, 
            wrap=tk.WORD,
            font=("Courier", 11)
        )
        self.lexical_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Syntax Analysis Tab
        syntax_frame = ttk.Frame(self.notebook)
        self.notebook.add(syntax_frame, text="Syntax Analysis")
        
        syntax_label = ttk.Label(syntax_frame, text="Syntax Tree:")
        syntax_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.syntax_text = scrolledtext.ScrolledText(
            syntax_frame, 
            wrap=tk.WORD,
            font=("Courier", 11)
        )
        self.syntax_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Grammar Analysis Tab
        grammar_frame = ttk.Frame(self.notebook)
        self.notebook.add(grammar_frame, text="Grammar Analysis")
        
        grammar_label = ttk.Label(grammar_frame, text="Grammar Rules:")
        grammar_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.grammar_text = scrolledtext.ScrolledText(
            grammar_frame, 
            wrap=tk.WORD,
            font=("Courier", 11)
        )
        self.grammar_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')
    
    def analyze_text(self):
        """Analyze the input text and display lexical, syntax, and grammar analysis"""
        # Get the input text
        input_text = self.input_text.get("1.0", tk.END).strip()
        
        if not input_text:
            self.lexical_text.delete("1.0", tk.END)
            self.lexical_text.insert("1.0", "Please enter some C code.")
            return
        
        try:
            # Analyze C code
            self.analyze_c_code(input_text)
            
        except Exception as e:
            error_msg = f"Error processing code: {str(e)}"
            self.lexical_text.delete("1.0", tk.END)
            self.lexical_text.insert("1.0", error_msg)
    
    def analyze_c_code(self, code):
        """Analyze C code input"""
        # Lexical Analysis
        tokens = self.tokenize_c_code(code)
        self.lexical_text.delete("1.0", tk.END)
        self.lexical_text.insert("1.0", "C Code Tokens:\n" + "\n".join(f"{token_type}: {token_value}" for token_type, token_value in tokens))
        
        # Syntax Analysis
        syntax_tree = self.build_c_syntax_tree(code)
        self.syntax_text.delete("1.0", tk.END)
        self.syntax_text.insert("1.0", syntax_tree)
        
        # Grammar Analysis
        grammar_rules = self.analyze_c_grammar(code)
        self.grammar_text.delete("1.0", tk.END)
        self.grammar_text.insert("1.0", grammar_rules)
    
    def tokenize_c_code(self, code):
        """Tokenize C code into meaningful components"""
        tokens = []
        lines = code.split('\n')
        
        # C keywords
        c_keywords = {
            'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
            'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if',
            'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof', 'static',
            'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while'
        }
        
        # C operators
        c_operators = {
            '+', '-', '*', '/', '%', '++', '--', '=', '+=', '-=', '*=', '/=', '%=',
            '==', '!=', '>', '<', '>=', '<=', '&&', '||', '!', '&', '|', '^', '~',
            '<<', '>>', '->', '.', '?', ':', ';', ',', '(', ')', '[', ']', '{', '}'
        }
        
        for line in lines:
            # Skip empty lines
            if not line.strip():
                continue
            
            # Handle preprocessor directives
            if line.strip().startswith('#'):
                tokens.append(('PREPROCESSOR', line.strip()))
                continue
            
            # Handle comments
            if '//' in line:
                comment_start = line.find('//')
                code_part = line[:comment_start]
                comment_part = line[comment_start:]
                if code_part.strip():
                    self._tokenize_line(code_part, tokens, c_keywords, c_operators)
                tokens.append(('COMMENT', comment_part))
                continue
            
            # Handle multi-line comments
            if '/*' in line:
                tokens.append(('COMMENT_START', '/*'))
                continue
            if '*/' in line:
                tokens.append(('COMMENT_END', '*/'))
                continue
            
            # Tokenize the line
            self._tokenize_line(line, tokens, c_keywords, c_operators)
        
        return tokens
    
    def _tokenize_line(self, line, tokens, c_keywords, c_operators):
        """Helper function to tokenize a single line of C code"""
        # Split the line into words
        words = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*|[0-9]+|"[^"]*"|\'[^\']*\'|[-+*/%=<>!&|^~?:;,.()\[\]{}]|->|\.', line)
        
        for word in words:
            if word in c_keywords:
                tokens.append(('KEYWORD', word))
            elif word in c_operators:
                tokens.append(('OPERATOR', word))
            elif word.startswith('"') or word.startswith("'"):
                tokens.append(('STRING', word))
            elif word.isdigit():
                tokens.append(('NUMBER', word))
            elif re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', word):
                tokens.append(('IDENTIFIER', word))
            else:
                tokens.append(('UNKNOWN', word))
    
    def build_c_syntax_tree(self, code):
        """Build a syntax tree for C code"""
        tree = []
        current_level = 0
        in_function = False
        in_block = False
        
        for line in code.split('\n'):
            if not line.strip():
                continue
            
            # Skip comments
            if line.strip().startswith('//') or '/*' in line or '*/' in line:
                continue
            
            # Calculate indentation level
            indent = len(line) - len(line.lstrip())
            level = indent // 4  # Assuming 4 spaces per indentation level
            
            # Handle function definitions
            if re.match(r'^\s*\w+\s+\w+\s*\([^)]*\)\s*\{?$', line):
                in_function = True
                tree.append('  ' * level + '└── Function: ' + line.strip())
                continue
            
            # Handle control structures
            if re.match(r'^\s*(if|for|while|do|switch)\s*\(', line):
                tree.append('  ' * level + '└── Control: ' + line.strip())
                in_block = True
                continue
            
            # Handle blocks
            if '{' in line:
                tree.append('  ' * level + '└── Block Start')
                in_block = True
                continue
            if '}' in line:
                tree.append('  ' * level + '└── Block End')
                in_block = False
                continue
            
            # Handle statements
            if ';' in line:
                tree.append('  ' * level + '└── Statement: ' + line.strip())
                continue
            
            # Handle other lines
            tree.append('  ' * level + '└── ' + line.strip())
        
        return '\n'.join(tree)
    
    def analyze_c_grammar(self, code):
        """Analyze C code grammar and structure"""
        rules = []
        
        # Check for main function
        if re.search(r'int\s+main\s*\([^)]*\)', code):
            rules.append("✓ Main function found")
        else:
            rules.append("✗ Main function not found")
        
        # Check for proper header inclusion
        if re.search(r'#include\s+<[^>]+>', code):
            rules.append("✓ Header files included")
        
        # Check for function definitions
        functions = re.findall(r'\w+\s+\w+\s*\([^)]*\)', code)
        if functions:
            rules.append(f"✓ Found {len(functions)} function(s):")
            for func in functions:
                rules.append(f"  - {func}")
        
        # Check for control structures
        if re.search(r'if\s*\([^)]*\)', code):
            rules.append("✓ If statements present")
        if re.search(r'for\s*\([^)]*\)', code):
            rules.append("✓ For loops present")
        if re.search(r'while\s*\([^)]*\)', code):
            rules.append("✓ While loops present")
        
        # Check for proper block structure
        open_braces = code.count('{')
        close_braces = code.count('}')
        if open_braces == close_braces:
            rules.append("✓ Balanced braces")
        else:
            rules.append(f"✗ Unbalanced braces: {open_braces} opening, {close_braces} closing")
        
        # Check for variable declarations
        if re.search(r'\w+\s+\w+\s*=', code):
            rules.append("✓ Variable declarations found")
        
        # Check for proper semicolon usage
        statements = code.count(';')
        if statements > 0:
            rules.append(f"✓ Found {statements} statements")
        
        # Check for proper indentation
        lines = code.split('\n')
        indent_levels = [len(line) - len(line.lstrip()) for line in lines if line.strip()]
        if all(level % 4 == 0 for level in indent_levels):
            rules.append("✓ Proper indentation (4 spaces)")
        else:
            rules.append("✗ Inconsistent indentation")
        
        return "\n".join(rules)


# Run the application
if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    app = LexicalAnalyzerApp(root)
    root.mainloop()