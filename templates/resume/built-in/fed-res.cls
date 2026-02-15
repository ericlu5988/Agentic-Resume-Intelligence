% Federal Resume Class File
\ProvidesClass{fed-res}
\NeedsTeXFormat{LaTeX2e}

\DeclareOption{draft}{\setlength\overfullrule{5pt}}
\DeclareOption{final}{\setlength\overfullrule{0pt}}
\DeclareOption*{%
  \PassOptionsToClass{\CurrentOption}{article}
}
\ProcessOptions\relax
\LoadClass{article}

% Ensure that generate pdf is machine readable/ATS parsable (PDFTeX only)
\RequirePackage{iftex}
\ifpdftex
  \pdfgentounicode=1
  \input{glyphtounicode}
\fi

%-------------------------------------------------------------------------------
%                3rd party packages
%-------------------------------------------------------------------------------
\RequirePackage{latexsym}
\RequirePackage[empty]{fullpage}
\RequirePackage{titlesec}
\RequirePackage{marvosym}
\RequirePackage[usenames,dvipsnames]{color}
\RequirePackage{verbatim}
\RequirePackage{enumitem}
\RequirePackage[hidelinks]{hyperref}
\RequirePackage{fancyhdr}
\RequirePackage[english]{babel}
\RequirePackage{csquotes}
\RequirePackage{tabularx}
\RequirePackage[export]{adjustbox}
\RequirePackage{indentfirst}

\usepackage[backend=biber,style=authoryear,sorting=ydnt, maxbibnames=1, minbibnames=1,uniquelist=false]{biblatex}
\setlength\bibitemsep{1em}

%-------------------------------------------------------------------------------
%                Configuration for document layout and style
%-------------------------------------------------------------------------------
\pagestyle{fancy}
\fancyhf{}
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
\setlength{\footskip}{4.4pt}

\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}

\urlstyle{same}
\raggedbottom
\raggedright
\setlength{\tabcolsep}{0pt}

\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large
}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

%-------------------------------------------------------------------------------
%                Configuration for resume entry elements
%-------------------------------------------------------------------------------
\newcommand{\resumeItem}[1]{
  \item{
    {#1 \vspace{-2pt}}
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{#3} & \textit{ #4} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubheadingShort}[2]{
  \vspace{-2pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubheadingWork}[6]{
  \vspace{-2pt}\item
    \begin{tabularx}{0.97\textwidth}[t]{l >{\raggedleft\arraybackslash}X}
      \textbf{#1} & #2 \\
      \textit{#3} & \textit{ #4} \\
    \end{tabularx}
    \begin{tabularx}{0.97\textwidth}[t]{l >{\raggedleft\arraybackslash}X}
      #5 & #6 \\
    \end{tabularx}\vspace{-7pt}
}

\newcommand{\resumeSubSubheading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \textit{#1} & \textit{ #2} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeProjectHeading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      #1 & #2 \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubItem}[1]{\resumeItem{#1}\vspace{-4pt}}
\renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}

\newcommand*{\cvpub}[1]{%
	\leftskip 1.1cm
    \parindent -0.7cm
    {#1}\vspace{3pt}
}