from enum import Enum


class FormErrorMessage(Enum):
    REQUIRED = "필수항목입니다."
    PASSWORD_CONFLICT = "비밀번호가 일치하지 않습니다."


class AccountErrorMessage(Enum):
    ACCOUNT_CANNOT_VALIDATE = "자격 증명을 검증할 수 없습니다."
    ACCOUNT_EXISTS = "이미 존재하는 회원입니다."
    ACCOUNT_NOT_FOUND = "계정을 찾을 수 없습니다.."
    ACCOUNT_DIFFERENT_DATA = "아이디 또는 비밀번호가 일치하지 않습니다."
    ACCOUNT_DIFFERENT_ACCOUNT = "다른 계정입니다."


class ReviewErrorMessage(Enum):
    REVIEW_NOT_FOUND = "후기를 찾을 수 없습니다."
    REVIEW_CANNOT_LIKE = "이미 비추천한 후기입니다."
    REVIEW_CANNOT_DISLIKE = "이미 추천한 후기입니다."


class CommentErrorMessage(Enum):
    COMMENT_NOT_FOUND = "댓글을 찾을 수 없습니다."
    COMMENT_CANNOT_LIKE = "이미 비추천한 댓글입니다."
    COMMENT_CANNOT_DISLIKE = "이미 추천한 댓글입니다."


class ETCErrorMessage(Enum):
    AUTHOR_CONFLICT_UPDATE = "수정 권한이 없습니다."
    AUTHOR_CONFLICT_DELETE = "삭제 권한이 없습니다."
