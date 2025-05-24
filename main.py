import tkinter as tk
from tkinter import ttk, font, messagebox, scrolledtext
import re
from collections import defaultdict

class LexicalAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg='#f0f2f5')  # Light gray background
        self.root.title("C Code Analyzer")
        self.root.geometry("1200x800")  # Slightly larger window
        
        # Configure window to be centered
        self.center_window()
        
        # Set up fonts
        title_font = font.Font(family="Helvetica", size=14, weight="bold")
        label_font = font.Font(family="Helvetica", size=11)
        text_font = font.Font(family="Consolas", size=11)
        
        # Create main frame with padding
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            self.main_frame,
            text="C Code Analysis Tool",
            font=title_font,
            background='#f0f2f5'
        )
        title_label.pack(pady=(0, 20))
        
        # Create a frame for the parallel layout
        parallel_frame = ttk.Frame(self.main_frame)
        parallel_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left side - Input section
        left_frame = ttk.Frame(parallel_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        input_label = ttk.Label(
            left_frame,
            text="Input C Code:",
            font=label_font,
            background='#f0f2f5'
        )
        input_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Style for text areas
        text_style = {
            'height': 15,
            'width': 40,
            'wrap': tk.WORD,
            'font': text_font,
            'bg': 'white',
            'fg': 'black',
            'insertbackground': 'black',
            'selectbackground': '#3498db',
            'selectforeground': 'white',
            'relief': 'solid',
            'borderwidth': 1
        }
        
        self.input_text = scrolledtext.ScrolledText(
            left_frame,
            **text_style
        )
        self.input_text.pack(fill=tk.BOTH, expand=True)
        
        # Right side - Output section
        right_frame = ttk.Frame(parallel_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        output_label = ttk.Label(
            right_frame,
            text="Analysis Result:",
            font=label_font,
            background='#f0f2f5'
        )
        output_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.output_text = scrolledtext.ScrolledText(
            right_frame,
            **text_style
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Buttons frame with styling
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)
        
        # Style for buttons
        button_style = {
            'padding': (15, 8),
            'style': 'Accent.TButton'
        }
        
        # Create custom style for buttons
        style = ttk.Style()
        style.configure(
            'Accent.TButton',
            font=('Helvetica', 10, 'bold'),
            background='#3498db',
            foreground='black'
        )
        
        # Analysis buttons
        self.lexical_button = ttk.Button(
            button_frame,
            text="Lexical Analysis",
            command=self.analyze_lexical,
            **button_style
        )
        self.lexical_button.pack(side=tk.LEFT, padx=5)
        
        self.syntax_button = ttk.Button(
            button_frame,
            text="Syntax Analysis",
            command=self.analyze_syntax,
            **button_style
        )
        self.syntax_button.pack(side=tk.LEFT, padx=5)
        
        self.grammar_button = ttk.Button(
            button_frame,
            text="Grammar Analysis",
            command=self.analyze_grammar,
            **button_style
        )
        self.grammar_button.pack(side=tk.LEFT, padx=5)
    
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')
    
    def analyze_lexical(self):
        """Perform lexical analysis"""
        input_text = self.input_text.get("1.0", tk.END).strip()
        if not input_text:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", "Please enter some C code.")
            return
        
        # First check syntax
        syntax_errors = self.validate_syntax(input_text)
        if syntax_errors:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", "Cannot perform lexical analysis due to syntax errors.\nPlease fix the syntax errors first.")
            return
        
        try:
            tokens = self.tokenize_c_code(input_text)
            result = "=== Lexical Analysis ===\n"
            result += "\n".join(f"{token_type}: {token_value}" for token_type, token_value in tokens)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", result)
        except Exception as e:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", f"Error in lexical analysis: {str(e)}")
    
    def analyze_syntax(self):
        """Perform syntax analysis"""
        input_text = self.input_text.get("1.0", tk.END).strip()
        if not input_text:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", "Please enter some C code.")
            return
        
        # Check syntax and get detailed errors
        syntax_errors = self.validate_syntax(input_text)
        if syntax_errors:
            result = "=== Syntax Analysis ===\n\n"
            result += "Syntax Errors Found:\n"
            for error in syntax_errors:
                result += f"\nLine {error['line']}: {error['message']}\n"
                result += f"Code: {error['code']}\n"
                result += f"      {' ' * error['position']}^\n"
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", result)
            return
        
        try:
            syntax_tree = self.build_c_syntax_tree(input_text)
            result = "=== Syntax Analysis ===\n"
            result += "No syntax errors found.\n\n"
            result += "Syntax Tree:\n"
            result += syntax_tree
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", result)
        except Exception as e:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", f"Error in syntax analysis: {str(e)}")
    
    def analyze_grammar(self):
        """Perform grammar analysis"""
        input_text = self.input_text.get("1.0", tk.END).strip()
        if not input_text:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", "Please enter some C code.")
            return
        
        # First check syntax
        syntax_errors = self.validate_syntax(input_text)
        if syntax_errors:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", "Cannot perform grammar analysis due to syntax errors.\nPlease fix the syntax errors first.")
            return
        
        try:
            grammar_rules = self.analyze_c_grammar(input_text)
            result = "=== Grammar Analysis ===\n"
            result += grammar_rules
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", result)
        except Exception as e:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", f"Error in grammar analysis: {str(e)}")
    
    def validate_syntax(self, code):
        """Validate basic C syntax and return detailed errors"""
        errors = []
        lines = code.split('\n')
        
        # Check for main function
        has_main = False
        for i, line in enumerate(lines, 1):
            if re.search(r'^\s*int\s+main\s*\([^)]*\)\s*\{?', line):
                has_main = True
                break
        if not has_main:
            errors.append({
                'line': 1,
                'position': 0,
                'message': "Missing main function",
                'code': "Program must contain a main function"
            })
        
        # Track state
        brace_stack = []
        paren_stack = []
        in_comment = False
        in_string = False
        string_char = None
        in_preprocessor = False
        in_switch_case = False
        
        for i, line in enumerate(lines, 1):
            j = 0
            while j < len(line):
                char = line[j]
                
                # Handle preprocessor directives
                if j == 0 and line.strip().startswith('#'):
                    in_preprocessor = True
                    break
                
                # Skip checking in preprocessor lines
                if in_preprocessor:
                    break
                
                # Handle comments
                if not in_string:
                    if char == '/' and j + 1 < len(line):
                        if line[j + 1] == '/':
                            break  # Skip rest of line for single-line comments
                        elif line[j + 1] == '*':
                            in_comment = True
                            j += 1
                    elif char == '*' and j + 1 < len(line) and line[j + 1] == '/':
                        if not in_comment:
                            errors.append({
                                'line': i,
                                'position': j,
                                'message': "Unexpected comment end '*/'",
                                'code': line
                            })
                        in_comment = False
                        j += 1
                
                # Handle strings
                if not in_comment:
                    if char in ['"', "'"]:
                        if not in_string:
                            in_string = True
                            string_char = char
                        elif char == string_char and line[j-1] != '\\':  # Handle escaped quotes
                            in_string = False
                
                # Only check braces and parentheses when not in comments or strings
                if not in_comment and not in_string:
                    if char == '{':
                        brace_stack.append((i, j))
                    elif char == '}':
                        if not brace_stack:
                            errors.append({
                                'line': i,
                                'position': j,
                                'message': "Unexpected closing brace '}'",
                                'code': line
                            })
                        else:
                            brace_stack.pop()
                    elif char == '(':
                        paren_stack.append((i, j))
                    elif char == ')':
                        if not paren_stack:
                            errors.append({
                                'line': i,
                                'position': j,
                                'message': "Unexpected closing parenthesis ')'",
                                'code': line
                            })
                        else:
                            paren_stack.pop()
                
                j += 1
            
            # Reset preprocessor state for next line
            in_preprocessor = False
        
        # Report unclosed braces and parentheses
        for line, pos in brace_stack:
            errors.append({
                'line': line,
                'position': pos,
                'message': "Unclosed brace '{'",
                'code': lines[line-1]
            })
        
        for line, pos in paren_stack:
            errors.append({
                'line': line,
                'position': pos,
                'message': "Unclosed parenthesis '('",
                'code': lines[line-1]
            })
        
        # Check for unclosed comments
        if in_comment:
            errors.append({
                'line': len(lines),
                'position': len(lines[-1]),
                'message': "Unclosed comment '/*'",
                'code': lines[-1]
            })
        
        # Check for unclosed strings
        if in_string:
            errors.append({
                'line': len(lines),
                'position': len(lines[-1]),
                'message': f"Unclosed string (started with {string_char})",
                'code': lines[-1]
            })
        
        # Check for basic C syntax patterns
        for i, line in enumerate(lines, 1):
            line = line.strip()
            
            # Skip empty lines, comments, and preprocessor directives
            if not line or line.startswith('//') or line.startswith('/*') or line.startswith('#'):
                continue
            
            # Check for switch-case statements
            if line.startswith('switch') or line.startswith('case') or line.startswith('default'):
                in_switch_case = True
                continue
            
            # Check for missing semicolons in statements
            if line and not line.endswith(';') and not line.endswith('{') and not line.endswith('}'):
                # Skip lines that are part of control structures or function declarations
                if not any(keyword in line for keyword in ['if', 'for', 'while', 'do', 'switch']):
                    # Skip function declarations and definitions
                    if not re.match(r'^\s*\w+\s+\w+\s*\([^)]*\)\s*\{?$', line):
                        # Check for statements that should end with semicolon
                        if (line.startswith('printf') or 
                            line.startswith('scanf') or 
                            line.startswith('return') or 
                            re.match(r'^\s*\w+\s*=', line) or 
                            re.match(r'^\s*(int|char|float|double|void)\s+\w+', line)):
                            errors.append({
                                'line': i,
                                'position': len(line),
                                'message': "Missing semicolon ';'",
                                'code': line
                            })
            
            # Check for proper if/for/while syntax
            for keyword in ['if', 'for', 'while']:
                if keyword in line:
                    # Check for balanced parentheses
                    open_count = line.count('(')
                    close_count = line.count(')')
                    if open_count != close_count:
                        errors.append({
                            'line': i,
                            'position': line.find(keyword) + len(keyword),
                            'message': f"Unbalanced parentheses in {keyword} statement",
                            'code': line
                        })
                    # Check for proper parentheses placement
                    elif not re.match(rf'^\s*{keyword}\s*\([^)]*\)', line):
                        # Skip if it's a printf or scanf statement
                        if not (line.startswith('printf') or line.startswith('scanf')):
                            errors.append({
                                'line': i,
                                'position': line.find(keyword) + len(keyword),
                                'message': f"Invalid {keyword} statement syntax",
                                'code': line
                            })
            
            # Check for proper variable declarations
            if re.match(r'^\s*(int|char|float|double|void)\s+\w+', line):
                if '=' in line and ';' not in line and not line.endswith('{'):
                    errors.append({
                        'line': i,
                        'position': len(line),
                        'message': "Missing semicolon in variable declaration",
                        'code': line
                    })
        
        return errors
    
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
